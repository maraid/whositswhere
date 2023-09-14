import auth
from datetime import datetime, timedelta
import logging
import pathlib
from requests import Session


PARKANIZER_API = "https://share.parkanizer.com/api"


class ParkanizerSession:
    def __init__(self, username: str, password: str):
        logging.info("Authenticating...")
        bearer_token: str = auth.get_token(username, password)
        logging.info("Authenticated")
        self.session: Session = Session()
        self.session.headers.update({"Authorization": bearer_token})

    def get_zones(self) -> list[dict[str, str]]:
        url = PARKANIZER_API + "/employee-desks/desk-marketplace/get-marketplace-zones"
        return self._post(url)["zones"]

    def get_employees(self) -> list[dict[str, str]]:
        url = PARKANIZER_API + "/employee-reservations/get-employees"
        # For some reason management people are not listed in today's query
        days_to_share = (datetime.today() + timedelta(days=32)).strftime(r"%Y-%m-%d")
        payload = {"daysToShare": [days_to_share]}
        return self._post(url, payload)['employeesOrNull']

    def get_desk_zone_map(self, zone_id: str, date) -> list[dict[str, str]]:
        url = PARKANIZER_API + "/employee-desks/desk-marketplace/get-marketplace-desk-zone-map"
        payload = {"date": date, "deskZoneId": zone_id}
        return self._post(url, payload)['mapOrNull']['desks']

    def get_employee_reservations(self, employee_id: str) -> list[dict[str, str]]:
        url = PARKANIZER_API + "/employee-desks/colleague-finder/get-colleague-desk-reservations"
        payload = {"colleagueId": employee_id}
        return self._post(url, payload)['deskReservations']

    def download_image(self, zone_id: str, out_path: str | pathlib.Path):
        url = PARKANIZER_API + "/components/desk-zone-map/desk-zone-map-image/" + zone_id
        response = self.session.get(url)
        if response.status_code == 200:
            with open(out_path, 'wb') as f:
                f.write(response.content)

    def _post(self, url, payload=None) -> dict:
        return self.session.post(url, json=payload).json()
