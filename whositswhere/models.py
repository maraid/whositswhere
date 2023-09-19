from dataclasses import dataclass, field


@dataclass
class NameBase:
    name: str


@dataclass
class Employee(NameBase):
    pass


@dataclass
class Desk(NameBase):
    x: float
    y: float
    radius: float
    reserved_by: None | Employee = None

    @property
    def is_free(self):
        return self.reserved_by is None


@dataclass
class Zone(NameBase):
    desks: dict[str, Desk] = field(default_factory=dict)


EmployeeMap = dict[str, Employee]
DeskMap = dict[str, Desk]
ZoneMap = dict[str, Zone]
