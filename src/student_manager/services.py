from student_manager.models import Student


def add_student(students: list[Student], student: Student) -> None:
    students.append(student)


def filter_by_group(students: list[Student], group: str) -> list[Student]:
    group = group.strip().upper()
    return [student for student in students if student.group == group]


def find_best_student(students: list[Student]) -> Student | None:
    if not students:
        return None
    best = students[0]
    for student in students[1:]:
        if student.average_grade > best.average_grade:
            best = student
    return best


def calculate_group_average(
    students: list[Student], group: str,
) -> float | None:
    selected = filter_by_group(students, group)
    if not selected:
        return None
    total = sum(student.average_grade for student in selected)
    return total / len(selected)


def sort_by_grade(students: list[Student]) -> list[Student]:
    return sorted(students, key=lambda student: student.average_grade,
                  reverse=True)
