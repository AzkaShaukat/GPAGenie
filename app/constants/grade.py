"""
Standard grade definitions and conversion constants
"""

# Standard 4.0 scale grade points
GRADE_POINTS = {
    'A+': 4.0,
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

# Percentage ranges for letter grades
PERCENTAGE_RANGES = {
    'A+': (97, 100),
    'A': (93, 96),
    'A-': (90, 92),
    'B+': (87, 89),
    'B': (83, 86),
    'B-': (80, 82),
    'C+': (77, 79),
    'C': (73, 76),
    'C-': (70, 72),
    'D+': (67, 69),
    'D': (65, 66),
    'F': (0, 64)
}

# Common international grade conversions
INTERNATIONAL_GRADES = {
    'UK': {
        'First Class': 4.0,
        'Upper Second': 3.3,
        'Lower Second': 2.7,
        'Third Class': 2.0,
        'Pass': 1.0,
        'Fail': 0.0
    },
    'Europe': {
        'A': 4.0,
        'B': 3.0,
        'C': 2.0,
        'D': 1.0,
        'E': 0.5,
        'F': 0.0
    }
}