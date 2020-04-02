"""Student-track matching algorithm"""

import csv
from typing import NamedTuple, Tuple, List, Dict, Optional


class Student(NamedTuple):
    """A student with his grades and wishes"""

    last_name: str
    first_name: str
    avg_grade: float
    wish_list: Tuple[str, ...]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} ({self.avg_grade})"


class Match(NamedTuple):
    """A match between a student and a track"""

    student: Student
    track_name: str
    wish_rank: int


def get_track_capacities() -> Dict[str, int]:
    """Return track capacities"""

    return {
        "Augmentation et Autonomie": 24,
        "Systèmes Cognitifs Hybrides": 24,
        "Intelligence Artificielle": 11,
        "Robotique": 10,
    }


def init_students() -> List[Student]:
    """Load students and their track wishes from CSV file"""

    student_list: List[Student] = []

    with open("students.csv", newline="") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Skip column names
        for row in reader:
            # Wishes are already sorted in CSV file
            wish_list = (row[3], row[4], row[5], row[6])
            student = Student(
                last_name=row[0],
                first_name=row[1],
                avg_grade=float(row[2]),
                wish_list=wish_list,
            )
            student_list.append(student)

    return student_list


def match_student(
    student: Student, track_count: Dict[str, int], track_capacities: Dict[str, int],
) -> Optional[Match]:
    """Match a student to a track according to his wishes, track count and track capacity"""

    rank = 0  # Try first wish
    track_name = student.wish_list[rank]

    # Iterate on student wishes to find a non-full track
    while track_count[track_name] == track_capacities[track_name] and rank < len(
        student.wish_list
    ):
        rank += 1  # Try next wish
        if rank < len(student.wish_list):
            track_name = student.wish_list[rank]

    if rank < len(student.wish_list):
        # A non-full track was found in student wishes
        return Match(student, track_name, rank + 1)

    # No track was found for this student
    return None


def match_students(
    student_list: List[Student], track_capacities: Dict[str, int]
) -> List[Match]:
    """Match students to tracks according to their merit, wishes and track capacities"""

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


def print_results(match_list: List[Match]) -> None:
    """Print results summary"""

    total_match_count = len(match_list)
    print(f"{total_match_count} affectations")

    track_capacities = get_track_capacities()
    track_count = len(track_capacities)

    # Print summary for wishes
    for rank in range(1, track_count):
        match_count = len([match for match in match_list if match.wish_rank == rank])
        match_percent: float = match_count / total_match_count
        print(
            f"Voeu {rank} : {match_count} affectation(s) ({match_percent * 100:.2f} %)"
        )

    # Print summary for tracks
    for track_name in track_capacities:
        student_count = len(
            [match for match in match_list if match.track_name == track_name]
        )
        print(f"{track_name} : {student_count} étudiants")


def save_results(match_list: List[Match]) -> None:
    """Save results to CSV file"""

    # Sort results by track name then student name
    sorted_match_list: List[Match] = sorted(
        match_list,
        key=lambda match: (
            match.track_name,
            match.student.last_name,
            match.student.first_name,
        ),
    )

    # Excel needs UTF8 with BOM encoding
    with open("results.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        # Write header (columns names)
        writer.writerow(["Nom", "Prénom", "Parcours", "Voeu"])
        for match in sorted_match_list:
            writer.writerow(
                [
                    match.student.last_name,
                    match.student.first_name,
                    match.track_name,
                    match.wish_rank,
                ]
            )


def main() -> None:
    """Main function"""

    student_list = init_students()
    track_capacities = get_track_capacities()

    print_input(student_list, track_capacities)

    # print("--- Liste des parcours ---")
    # print(*track_capacities, sep="\n")
    # print()

    # print("--- Liste des étudiants ---")
    # print(*student_list, sep="\n")
    # print()

    match_list = match_students(student_list, track_capacities)

    print_results(match_list)
    save_results(match_list)


if __name__ == "__main__":
    main()
