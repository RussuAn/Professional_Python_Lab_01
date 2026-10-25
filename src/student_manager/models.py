from dataclasses import dataclass
from math import isfinite


@dataclass
class Student:
    first_name: str
    last_name: str
    group: str
    average_grade: float

    def __post_init__(self) -> None:
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.group = self.group.strip().upper()
        if not self.first_name or not self.last_name or not self.group:
            raise ValueError(
                "Ім'я, прізвище та група не можуть бути порожніми."
            )
        if (not isfinite(self.average_grade)
                or not 0 <= self.average_grade <= 100):
            raise ValueError("Середній бал має бути числом від 0 до 100.")

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"
