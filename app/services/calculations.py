from typing import List, Dict, Tuple

GRADE_POINTS = {
    'A': 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1.0,
    'F': 0.0
}


def calculate_sgpa(subjects: List[Dict]) -> Tuple[float, List[Tuple[Dict, float]]]:
    """
    Calculate SGPA from list of subjects
    Returns: (sgpa, list of (subject, grade_point))
    """
    if not subjects:
        raise ValueError("At least one subject is required")

    total_grade_points = 0.0
    total_credits = 0
    results = []

    for subject in subjects:
        grade = subject['grade'].upper()
        if grade not in GRADE_POINTS:
            raise ValueError(f"Invalid grade: {grade}")

        credits = subject['credits']
        if not isinstance(credits, int) or credits < 1 or credits > 4:
            raise ValueError("Credits must be between 1 and 4")

        grade_point = GRADE_POINTS[grade]
        weighted_points = grade_point * credits

        total_grade_points += weighted_points
        total_credits += credits
        results.append((subject, grade_point))

    if total_credits == 0:
        raise ValueError("Total credits cannot be zero")

    sgpa = total_grade_points / total_credits
    return (sgpa, results)


def calculate_cgpa(semesters_data):
    """
    Calculate CGPA from list of semesters
    Returns: (cgpa, list of (semester, quality_points))
    """
    if not semesters_data:
        raise ValueError("At least one semester is required")

    total_quality_points = 0.0
    total_credits = 0
    semester_results = []

    for sem in semesters_data:
        quality_points = sem['sgpa'] * sem['credits']
        total_quality_points += quality_points
        total_credits += sem['credits']
        semester_results.append((sem, quality_points))

    if total_credits == 0:
        raise ValueError("Total credits cannot be zero")

    cgpa = total_quality_points / total_credits
    return (cgpa, semester_results)