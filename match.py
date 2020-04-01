"""Student-track matching algorithm"""

import csv
from typing import NamedTuple, Tuple, List


class Preference(NamedTuple):
    track_name: str
    rank: int


class Student(NamedTuple):
    last_name: str
    first_name: str
    avg_grade: float
    preference_list: Tuple[Preference]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.avg_grade})"


class Track(NamedTuple):
    name: str
    capacity: int

    def __str__(self):
        return f"{self.name} ({self.capacity} places)"


track_list: Tuple[Track] = (
    Track("Augmentation et Autonomie", 24),
    Track("Systèmes Cognitifs Hybrides", 24),
    Track("Intelligence Artificielle", 11),
    Track("Robotique", 10),
)

print("--- Liste des parcours ---")
print(*track_list, sep="\n")
print()

student_list: List[Student] = []
with open("students.csv", newline="") as file:
    reader = csv.reader(file, delimiter=";")
    next(reader)  # Skip column names
    for row in reader:
        preference_list: Tuple[Preference] = (Preference(row[3], 1))
        student = Student(
            last_name=row[0],
            first_name=row[1],
            avg_grade=row[2],
            preference_list=preference_list,
        )
        student_list.append(student)

print("--- Liste des étudiants ---")
print(*student_list, sep="\n")
