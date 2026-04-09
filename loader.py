import csv

def load_courses(filename, university):
    """Load course catalog and capacities from CSV
    Designed by: Mufeed Dudha"""
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            
            course_code = (row.get('course_id') or row.get('course_code') or '').strip()
            credits = row.get('credits')
            capacity = row.get('capacity', 100)

            if not course_code or not credits:
                continue
            try:
                credits = int(credits)
                capacity = int(capacity) if capacity else 100
                university.add_course(course_code, credits, capacity)
            except ValueError:
                pass

def load_students(filename, university):
    """
    Updated to match enrollments_CSE10.csv format:
    Columns: student_id, course_id, term, grade
    """
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            s_id = row.get('student_id')
            c_id = row.get('course_id')
            term = row.get('term', '2024-01-01') 
            grade = row.get('grade') or 'N/A'

            if not s_id or not s_id.startswith('S'):
                continue

            
            numeric_part = int(s_id.strip().lstrip('S'))
            formatted_id = f"STU{numeric_part:05d}"

            if formatted_id not in university.students:
                
                university.add_student(formatted_id, f"Student_{formatted_id}")

            student = university.get_student(formatted_id)
            course = university.get_course(c_id.strip())

           
            if student and course:
                try:
                    
                    student.enroll(course, grade, term)
                except ValueError as e:
                    
                    pass