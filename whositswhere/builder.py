from queries import ParkanizerSession
from models import Employee, EmployeeMap, Desk, DeskMap, Zone, ZoneMap
import logging


class ReservationMapBuilder:
    def __init__(self, session: ParkanizerSession, selected_date: str):
        self.session: ParkanizerSession = session
        self.selected_date: str = selected_date
        self.zones: ZoneMap = {}

    def build(self):
        self.zones = self._create_zones()
        logging.info(f"{len(self.zones)} zones fetched from server ")
        for key, zone in self.zones.items():
            zone.desks = self._create_desks(key)
            logging.info(f"{len(zone.desks)} desks was found for for zone [{zone.name}]")
        self._fill_reservations()
        return self.zones

    def _create_employees(self) -> EmployeeMap:
        json_employees = self.session.get_employees()
        return {e['employeeId']: Employee(e['fullName']) for e in json_employees}

    def _create_desks(self, zone_id: str) -> DeskMap:
        json_desks = self.session.get_desk_zone_map(zone_id, self.selected_date)
        return {d['id']: Desk(d['nameOrNull'], float(d['x']), float(d['y'])) for d in json_desks}

    def _create_zones(self) -> ZoneMap:
        json_zones = self.session.get_zones()
        return {z['id']: Zone(z['name']) for z in json_zones}

    def _fill_reservations(self) -> None:
        employees = self._create_employees()
        logging.info(f"{len(employees)} employees fetched from server")
        for key, emp in employees.items():
            logging.debug(f"Processing {emp.name}. ID: {key}")
            reservations = self.session.get_employee_reservations(key)
            for res in reservations:
                if res['date'] == self.selected_date:
                    zone = self.zones[res['deskZoneId']]
                    desk = zone.desks[res['deskId']]
                    desk.reserved_by = emp
                    logging.info(f"{emp.name} reserved {zone.name}:{desk.name}")
