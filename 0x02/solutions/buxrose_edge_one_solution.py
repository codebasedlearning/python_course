# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Buxrose Edge'

Topics
  - dictionaries
  - comprehensions
  - sorting
"""


MATH = "Math"
ENGLISH = "English"
PHYSICS = "Physics"

SUBJECTS = [MATH, ENGLISH, PHYSICS]

GRADES = {
    "Alice": {MATH: 85, ENGLISH: 78, PHYSICS: 92},
    "Bob": {MATH: 56, ENGLISH: 33, PHYSICS: 52},
    "Charlie": {MATH: 97, ENGLISH: 88, PHYSICS: 91},
    "Diana": {MATH: 42, ENGLISH: 30, PHYSICS: 36},
    "Eve": {MATH: 67, ENGLISH: 80, PHYSICS: 45},
}


# {'Alice': 85.0, 'Bob': 47.0, 'Charlie': 92.0, 'Diana': 36.0, 'Eve': 64.0}

def calc_average_grades():
    """ calc average grades for each student """

    # --- short variant ---
    average_grades = {student: sum(subjects.values()) / len(subjects)
                      for student, subjects in GRADES.items()}

    # --- explicit variant ---
    # average_grades = {}
    # for student, subjects in GRADES.items():
    #     total, count = 0, 0
    #     for grade in subjects.values():
    #         total += grade
    #         count += 1
    #     average_grades[student] = total / count
    return average_grades


# 'Charlie' with 92.00

def determine_top_performer(average_grades):
    """ determine top performer and highest average grade """

    # --- short variant ---
    top_student = max(average_grades, key=average_grades.get)
    # same as:  = max(average_grades, key=lambda student: average_grades[student])
    highest_average = average_grades[top_student]

    # --- explicit variant ---
    # highest_average = 0
    # top_student = None
    # for student, average in average_grades.items():
    #     if average > highest_average:
    #         highest_average = average
    #         top_student = student
    return top_student, highest_average


# ['Bob', 'Diana']

def determine_all_students_with_a_fail():
    """ determine all students with a fail """

    # --- short variant ---
    students_below_40 = [student for student, subjects in GRADES.items()
                         if any(grade < 40 for grade in subjects.values())]

    # --- explicit variant ---
    # students_below_40 = []
    # for student, subjects in GRADES.items():
    #     below_40 = False
    #     for grade in subjects.values():
    #         if grade < 40:
    #             below_40 = True
    #             break
    #     if below_40:
    #         students_below_40.append(student)
    return students_below_40


# ['Math']

def determine_subjects_everyone_passed():
    """ determine subjects everyone passed """

    # --- short variant ---
    passed_subjects = [subject for subject in SUBJECTS
                       if all(grades[subject] >= 40 for grades in GRADES.values())]
    # or:             [subject for subject in SUBJECTS
    #                  if all(GRADES[student][subject] >= 40 for student in GRADES)]

    # --- explicit variant ---
    # passed_subjects = []
    # for subject in SUBJECTS:
    #     all_passed = True
    #     for student, subjects in GRADES.items():
    #         if subjects[subject] < 40:
    #             all_passed = False
    #             break
    #     if all_passed:
    #         passed_subjects.append(subject)
    return passed_subjects


# ['Charlie', 'Alice', 'Eve', 'Bob', 'Diana']

def sort_students_by_average_grade(average_grades):
    """ sort students by average grade """

    # --- short variant ---
    sorted_students = sorted(average_grades.items(), key=lambda x: x[1], reverse=True)
    student_names_sorted = [student for student, _ in sorted_students]

    # --- explicit variant (Insertion Sort) ---
    # sorted_students = []
    # for student, average in average_grades.items():
    #     inserted = False
    #     for i in range(len(sorted_students)):
    #         if average > sorted_students[i][1]:
    #             sorted_students.insert(i, (student, average))
    #             inserted = True
    #             break
    #     if not inserted:
    #         sorted_students.append((student, average))
    # student_names_sorted = [student for student, _ in sorted_students]
    return student_names_sorted


def solve():
    """ solve all sub-tasks """
    average_grades = calc_average_grades()
    print(f" 1| {average_grades=}")

    top_student, highest_average = determine_top_performer(average_grades)
    print(f" 2| {top_student=} with {highest_average:.2f}")

    students_below_40 = determine_all_students_with_a_fail()
    print(f" 3| {students_below_40=}")

    passed_subjects = determine_subjects_everyone_passed()
    print(f" 4| {passed_subjects=}")

    student_names_sorted = sort_students_by_average_grade(average_grades)
    print(f" 5| {student_names_sorted=}")


if __name__ == "__main__":
    solve()
