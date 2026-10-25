"""Перевірка операцій варіанта 1 та граничних випадків."""

import pytest

from student_manager.models import Student
from student_manager.services import (
    add_student,
    calculate_group_average,
    filter_by_group,
    find_best_student,
    sort_by_grade,
)


@pytest.fixture
def students() -> list[Student]:
    return [
        Student("Марія", "Дорош", "ФЕП-32", 86.5),
        Student("Данило", "Левицький", "ФЕП-31", 95.0),
        Student("Соломія", "Климчук", "ФЕП-32", 91.5),
    ]


def test_add_student(students: list[Student]) -> None:
    new_student = Student("Тарас", "Савчук", "ФЕП-32", 80.0)
    add_student(students, new_student)
    assert len(students) == 4
    assert students[-1] is new_student


def test_filter_group(students: list[Student]) -> None:
    result = filter_by_group(students, " феп-32 ")
    assert [student.last_name for student in result] == ["Дорош", "Климчук"]
    assert filter_by_group(students, "ФЕП-99") == []


def test_average_of_selected_group(students: list[Student]) -> None:
    assert calculate_group_average(students, "ФЕП-32") == pytest.approx(89.0)
    assert calculate_group_average(students, "ФЕП-31") == pytest.approx(95.0)
    assert calculate_group_average(students, "ФЕП-99") is None
    assert calculate_group_average([], "ФЕП-32") is None


def test_best_student(students: list[Student]) -> None:
    assert find_best_student(students) is students[1]
    assert find_best_student([]) is None
    add_student(students, Student("Іван", "Романюк", "ФЕП-32", 95.0))
    assert find_best_student(students) is students[1]


def test_sort_keeps_original_order(students: list[Student]) -> None:
    result = sort_by_grade(students)
    assert [student.average_grade for student in result] == [95.0, 91.5, 86.5]
    assert students[0].last_name == "Дорош"
    assert sort_by_grade([]) == []


@pytest.mark.parametrize("grade", [-0.1, 100.1, float("nan"), float("inf")])
def test_invalid_grade(grade: float) -> None:
    with pytest.raises(ValueError):
        Student("Марія", "Дорош", "ФЕП-32", grade)


@pytest.mark.parametrize("grade", [0.0, 100.0])
def test_grade_boundaries(grade: float) -> None:
    student = Student(" Марія ", " Дорош ", " феп-32 ", grade)
    assert student.full_name == "Дорош Марія"
    assert student.group == "ФЕП-32"
    assert student.average_grade == grade


@pytest.mark.parametrize("fields", [
    (" ", "Дорош", "ФЕП-32"),
    ("Марія", "", "ФЕП-32"),
    ("Марія", "Дорош", " "),
])
def test_empty_fields(fields: tuple[str, str, str]) -> None:
    with pytest.raises(ValueError):
        Student(*fields, 86.5)
