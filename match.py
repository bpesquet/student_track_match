"""Student-track matching algorithm"""

import csv
from typing import NamedTuple, Tuple, List, Dict, Optional


class Student(NamedTuple):
    last_name: str
    first_name: str
    avg_grade: float
    preference_list: Tuple[str]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.avg_grade})"


class Match(NamedTuple):
    student: Student
    track_name: str
    preference_rank: int


def get_track_capacities() -> Dict[str, int]:
    """Return track capacities"""

    return {
        "Augmentation et Autonomie": 24,
        "Systèmes Cognitifs Hybrides": 24,
        "Intelligence Artificielle": 11,
        "Robotique": 10,
    }


def init_students() -> List[Student]:
    """Load students and their track preferences from CSV file"""

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


def match_student(
    student: Student, track_count: Dict[str, int], track_capacities: Dict[str, int],
) -> Optional[Match]:
    """Match a student to a track according to his preferences, track count and track capacity"""

    rank = 0  # Try first preference
    track_name = student.preference_list[rank]

    # Iterate on student preferences to find a non-full track
    while track_count[track_name] == track_capacities[track_name] and rank < len(
        student.preference_list
    ):
        rank += 1  # Try next preference
        if rank < len(student.preference_list):
            track_name = student.preference_list[rank]

    if rank < len(student.preference_list):
        # A non-full track was found in student preferences
        return Match(student, track_name, rank + 1)

    # No track was found for this student
    return None


def match(student_list: List[Student], track_capacities: Dict[str, int]) -> List[Match]:
    """Match students to tracks according to their rank and preferences"""

    match_list: List[Match] = []

    # Sort students by merit (best grade first)
    sorted_student_list = sorted(
        student_list, key=lambda student: student.avg_grade, reverse=True
    )
    # print(*sorted_student_list, sep="\n")

    # Init student count to 0 for all tracks
    track_count: Dict[str, int] = dict.fromkeys(track_capacities.keys(), 0)

    for student in sorted_student_list:
        match = match_student(student, track_count, track_capacities)
        if match is not None:
            match_list.append(match)
            track_count[match.track_name] += 1
        else:
            print(f"ALERTE ! Aucun parcours disponible pour l'étudiant {student}")

    return match_list


def print_input(students: List[Student], track_capacities: Dict[str, int]) -> None:
    """Print input summary"""

    total_capacity: int = sum(track_capacities.values())
    print(
        f"{len(track_capacities)} parcours ({total_capacity} places) pour {len(students)} étudiants"
    )


def print_results(results: List[Match]) -> None:
    """Print results summary"""

    total_match_count = len(results)
    print(f"{total_match_count} affectations")

    track_capacities = get_track_capacities()
    track_count = len(track_capacities)

    # Print summary for ranks
    for rank in range(1, track_count):
        match_count = len([match for match in results if match.preference_rank == rank])
        match_percent: float = match_count / total_match_count
        print(
            f"Voeu {rank} : {match_count} affectation(s) ({match_percent * 100:.2f} %)"
        )

    # Print summary for tracks
    for track_name in track_capacities.keys():
        student_count = len(
            [match for match in results if match.track_name == track_name]
        )
        print(f"{track_name} : {student_count} étudiants")


def save_results(results: List[Match]) -> None:
    """Save results to CSV file"""

    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        for match in results:
            writer.writerow(
                [
                    match.student.last_name + " " + match.student.first_name,
                    match.track_name,
                    match.preference_rank,
                ]
            )


def main():
    student_list = init_students()
    track_capacities = get_track_capacities()

    print_input(student_list, track_capacities)

    # print("--- Liste des parcours ---")
    # print(*track_capacities, sep="\n")
    # print()

    # print("--- Liste des étudiants ---")
    # print(*student_list, sep="\n")
    # print()

    results = match(student_list, track_capacities)

    print_results(results)
    save_results(results)


if __name__ == "__main__":
    main()
