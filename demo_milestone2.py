import csv
from classes import University, recursive_binary_search
from loader import load_courses, load_students

def run_milestone2_demo():
    """ 
    Demonstrates Milestone 2 features: course loading, enrollment, waitlisting, 
    sorting, binary search dropping, and extra credit undo.
    Designed By: Mufeed Dudha
    """
    uni = University()

    # Load Course 
    print("Loading Courses")
    load_courses("course_catalog_CSE10_with_capacity.csv", uni)
    cse1010 = uni.get_course("CSE1010")
    
    
    cse1010.capacity = 5
    print(f"Loaded {cse1010.course_code}. Set demo capacity to: {cse1010.capacity}\n")

    # Load Students
    
    print("Loading Students and Enrollments")
    load_students("enrollments_CSE10.csv", uni)

    print(f"Enrolled Count: {len(cse1010.enrolled_roster)}")
    print(f"Waitlist Count: {len(cse1010.waitlist)}")
    
    if not cse1010.waitlist.is_empty():
        
        waitlisted_student = cse1010.waitlist.head.data[0]
        print(f"First Student on Waitlist: {waitlisted_student.student_id} ({waitlisted_student.name})\n")

    # Sorting
    
    cse1010.sort_enrolled(by='id', algorithm='insertion')
    current_ids = [r.student.student_id for r in cse1010.enrolled_roster]
    print(f"Sorted IDs: {current_ids}\n")

    # Binary Search & Dropping
    target_id = cse1010.enrolled_roster[0].student.student_id
    
    
    
    dropped_student = cse1010.drop(target_id)
    print(f"Successfully dropped: {dropped_student.name}")
    print(f"New Enrolled Count: {len(cse1010.enrolled_roster)} (Waitlist student was promoted!)")
    print(f"New Waitlist Count: {len(cse1010.waitlist)}\n")

    # Extra Credit
    
    undo_msg = cse1010.undo_action()
    print(f"Undo Result: {undo_msg}")
    print(f"Final Enrolled Count: {len(cse1010.enrolled_roster)}")

if __name__ == "__main__":
    run_milestone2_demo()