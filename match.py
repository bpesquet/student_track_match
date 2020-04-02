"""Student-track matching algorithm"""

import csv
from typing import NamedTuple, Tuple, List


class Student(NamedTuple):
    last_name: str
    first_name: str
    avg_grade: float
    preference_list: Tuple[str]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.avg_grade}) - {self.preference_list}"


class Track(NamedTuple):
    name: str
    capacity: int

    def __str__(self):
        return f"{self.name} ({self.capacity} places)"


class Match(NamedTuple):
    student_last_name: str
    student_first_name: str
    track_name: str
    preference_rank: int


def init_tracks() -> Tuple[Track]:
    """Init tracks"""

    return (
        Track("Augmentation et Autonomie", 24),
        Track("Systèmes Cognitifs Hybrides", 24),
        Track("Intelligence Artificielle", 11),
        Track("Robotique", 10),
    )


def init_students() -> List[Student]:
    """Load students and their preferences from CSV file"""

    student_list: List[Student] = []

    with open("students.csv", newline="") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Skip column names
        for row in reader:
            # Preferences are already sorted in CSV file
            preference_list = (row[3], row[4], row[5], row[6])
            student = Student(
                last_name=row[0],
                first_name=row[1],
                avg_grade=row[2],
                preference_list=preference_list,
            )
            student_list.append(student)

    return student_list


def get_capacity(track_list: Tuple[Track], track_name: str) -> int:
    return [track.capacity for track in track_list if track.name == track_name][0]


track_list = init_tracks()
student_list = init_students()

print("--- Liste des parcours ---")
print(*track_list, sep="\n")
print()

print("--- Liste des étudiants ---")
print(*student_list, sep="\n")

# Sort students by merit (best grade first)
sorted_student_list = sorted(
    student_list, key=lambda student: student.avg_grade, reverse=True
)
print(*sorted_student_list, sep="\n")

match_list: List[Match] = []

for student in sorted_student_list:
    rank: int = 0
    # while get_capacity(track_list, student.preference_list[rank])
