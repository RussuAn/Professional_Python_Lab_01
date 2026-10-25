"""Консольне меню системи обліку студентів."""

from student_manager.models import Student
from student_manager.services import (
    add_student,
    calculate_group_average,
    filter_by_group,
    find_best_student,
    sort_by_grade,
)


def print_students(students: list[Student]) -> None:
    if not students:
        print("Студентів не знайдено.")
        return
    print(f"{'Прізвище та ім’я':30} {'Група':10} {'Середній бал':>12}")
    print("-" * 54)
    for student in students:
        print(f"{student.full_name:30} {student.group:10} "
              f"{student.average_grade:12.2f}")


def read_student() -> Student:
    first_name = input("Ім'я: ")
    last_name = input("Прізвище: ")
    group = input("Група: ")
    try:
        grade = float(input("Середній бал (0–100): ").replace(",", "."))
    except ValueError:
        raise ValueError("Середній бал потрібно ввести числом.") from None
    return Student(first_name, last_name, group, grade)


def print_menu() -> None:
    print("\n1. Додати студента")
    print("2. Показати всіх студентів")
    print("3. Знайти студентів за групою")
    print("4. Визначити найкращого студента")
    print("5. Обчислити середній бал групи")
    print("6. Показати рейтинг за середнім балом")
    print("0. Завершити роботу")


def main() -> None:
    students: list[Student] = []
    print("СИСТЕМА ОБЛІКУ СТУДЕНТІВ")
    while True:
        print_menu()
        command = input("Оберіть дію: ").strip()
        if command == "0":
            print("Роботу завершено.")
            break
        if command == "1":
            try:
                student = read_student()
                add_student(students, student)
                print(f"Додано: {student.full_name}.")
            except ValueError as error:
                print(f"Помилка: {error}")
        elif command == "2":
            print_students(students)
        elif command == "3":
            group = input("Група для пошуку: ")
            print_students(filter_by_group(students, group))
        elif command == "4":
            best = find_best_student(students)
            if best is None:
                print("Список порожній. Спочатку додайте студентів.")
            else:
                print("Найкращий студент:")
                print_students([best])
        elif command == "5":
            group = input("Група для обчислення: ").strip().upper()
            average = calculate_group_average(students, group)
            if average is None:
                print("У цій групі немає студентів.")
            else:
                print(f"Середній бал групи {group}: {average:.2f}")
        elif command == "6":
            print_students(sort_by_grade(students))
        else:
            print("Такої дії немає. Оберіть пункт від 0 до 6.")


if __name__ == "__main__":
    main()
