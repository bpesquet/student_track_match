"""
Student/track matching script
"""

import csv
import sys
from typing import NamedTuple, Tuple, List, Dict, Optional
from dataclasses import dataclass, field


def get_semester_weights() -> Dict[str, int]:
    """Return semester weights used to compute students' average grade"""

    # Order must match grades order in students CSV file
    return {"S5": 1, "S6": 1, "S7": 2, "S8": 2}


def get_track_capacities() -> Dict[str, int]:
    """Return track capacities (maximum number of students)"""

    # Names must exactly match track names in students CSV file
    return {
        "Augmentation et Autonomie": 24,
        "Systèmes Cognitifs Hybrides": 24,
        "Intelligence Artificielle": 24,
        "Robotique": 10,
    }


@dataclass
class Student:
    """A student with his grades and track wishes"""

    last_name: str
    first_name: str
    grade_list: Dict[str, Optional[float]]
    wish_list: Tuple[str, ...]
    avg_grade: float = field(init=False, repr=False)  # Computed after init

    def __post_init__(self) -> None:
        self.avg_grade = self.__compute_avg_grade()

    def __compute_avg_grade(self) -> float:
        """Compute and return weighted average of student grades"""

        weighted_grade_sum: float = 0
        weight_count: int = 0
        semester_weights: Dict[str, int] = get_semester_weights()

        # Compute weighted sum of student grades
        for (semester, grade) in self.grade_list.items():
            if semester in semester_weights:
                if grade is not None:
                    weight = semester_weights[semester]
                    weighted_grade_sum += grade * weight
                    weight_count += weight
            else:
                print(
                    f"ALERTE ! Semestre {semester} non trouvé dans le dictionnaire des poids"
                )

        if weighted_grade_sum > 0:
            return weighted_grade_sum / weight_count

        print(f"ALERTE ! Aucune note trouvée pour l'étudiant(e) {self}")
        return 0

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


class Match(NamedTuple):
    """A match between a student and a track"""

    student: Student
    track_name: str
    wish_rank: int


def french_float(value: str) -> Optional[float]:
    """Convert a string containing a comma-separated float value into a float"""

    if value == "":
        return None

    fixed_value = value.replace(",", ".")
    return float(fixed_value)


def init_students(file_name: str) -> List[Student]:
    """
    Load students with grades and track wishes from CSV file

    The student CSV file must contain one line per student, with the following format:
      last name, first name, grades for past 4 semesters, wishes for all tracks
    """

    student_list: List[Student] = []
    # Used to iterate on semester names by index
    semester_names = list(get_semester_weights().keys())

    with open(file_name, newline="") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Skip column names

        for row in reader:
            grade_list: Dict[str, Optional[float]] = {}
            # Grades are ordered by semester in columns 3 to 6 of CSV file
            for i in range(4):
                grade_list[semester_names[i]] = french_float(row[i + 2])

            # Wishes are ordered by preference in columns 7 to 10 of CSV file
            wish_list: Tuple[str, ...] = (row[6], row[7], row[8], row[9])

            student = Student(
                last_name=row[0],
                first_name=row[1],
                grade_list=grade_list,
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

    # Init assigned student count to 0 for all tracks
    track_count: Dict[str, int] = dict.fromkeys(track_capacities.keys(), 0)

    for student in sorted_student_list:
        match = match_student(student, track_count, track_capacities)
        if match is not None:
            match_list.append(match)
            track_count[match.track_name] += 1
        else:
            print(f"ALERTE ! Aucun parcours disponible pour l'étudiant(e) {student}")

    return match_list


def print_input(
    student_list: List[Student],
    track_capacities: Dict[str, int],
    semester_weights: Dict[str, int],
) -> None:
    """Print input summary"""

    print("--- Données d'entrée ---")
    total_capacity: int = sum(track_capacities.values())
    print(
        f"{len(track_capacities)} parcours ({total_capacity} places) pour {len(student_list)} étudiants"
    )
    for (name, capacity) in track_capacities.items():
        print(f"{name} : {capacity} places")
    print(f"Poids des semestres dans le calcul de la moyenne : {semester_weights}")


def save_input(student_list: List[Student]) -> None:
    """Save input to CSV file"""

    # Sort students by merit (best grade first)
    sorted_student_list = sorted(
        student_list, key=lambda student: student.avg_grade, reverse=True
    )

    # Excel needs UTF8 with BOM encoding
    with open("classement.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        # Write header (columns names)
        writer.writerow(["Nom", "Prénom", "Moyenne", "Voeu 1"])
        for student in sorted_student_list:
            writer.writerow(
                [
                    student.last_name,
                    student.first_name,
                    student.avg_grade,
                    student.wish_list[0],
                ]
            )


def print_results(match_list: List[Match], track_capacities: Dict[str, int]) -> None:
    """Print results summary"""

    print("--- Résultats ---")
    total_match_count = len(match_list)
    print(f"{total_match_count} affectations")

    track_count = len(track_capacities)

    # Print summary for wishes
    for rank in range(1, track_count + 1):
        match_count = len([match for match in match_list if match.wish_rank == rank])
        match_percent: float = match_count / total_match_count
        if match_count > 0:
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
    with open("affectations.csv", "w", newline="", encoding="utf-8-sig") as file:
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


def main(student_file_name: str) -> None:
    """Main function"""

    student_list = init_students(student_file_name)
    track_capacities = get_track_capacities()

    print_input(student_list, track_capacities, get_semester_weights())
    save_input(student_list)

    match_list = match_students(student_list, track_capacities)

    print_results(match_list, track_capacities)
    save_results(match_list)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(student_file_name=sys.argv[1])
    else:
        print("Veuillez fournir le nom du fichier CSV des étudiants")
