from classes import University, merge_sort, quick_sort, recursive_binary_search
from loader import load_courses, load_students, load_prerequisites

def run_milestone3_demo():
    """ Demonstrates Milestone 3 features: HashMap, prerequisite checking, waitlist management, sorting, binary search, and undo functionality.
    Designed by: Mufeed Dudha"""
    print("-" * 50)
    print("   UNIVERSITY SYSTEM MILESTONE 3 DEMO")
    print("")
    

    uni = University()

    # Loading data
    
    load_courses("course_catalog_CSE10_with_capacity.csv", uni)
    load_students("enrollments_CSE10.csv", uni)
    load_prerequisites("cse_prerequisites.csv", uni)

    # Hashmap verification
    print("Hashmap verification")
    test_student_id = "STU00164"
    
    student = uni.students.get(test_student_id)
    if student:
        print(f"HashMap Lookup Success: Found {student.name} ({student.student_id})")
    print("")

    # Prequisite checking
    print("Prequisite checking")
    cse2050 = uni.get_course("CSE2050") # prereq: CSE1010
    new_stu = uni.add_student("STU99999", "Demo Student")
    
    print(f"Attempting to enroll {new_stu.name} in {cse2050.course_code}...")
    print(f"(Required Prerequisite: {cse2050.prerequisite})")
    
    try:
        cse2050.request_enroll(new_stu, "N/A", "2026-01-01")
    except ValueError as e:
        print(f"Enrollment Blocked: {e}")

    print("\nAdding prerequisite credit (CSE1010: A) to student...")
    new_stu.courses.put("CSE1010", "A") # Manually adding to HashMap
    
    try:
        msg = cse2050.request_enroll(new_stu, "N/A", "2026-01-01")
        print(f"Enrollment Success: {msg}")
    except ValueError as e:
        print(f"Error: {e}")
    print("")

    # Waitlist and capacity management
    print("Waitlist and capacity management")
    cse2050 = uni.get_course("CSE2050")
    print(f"Course {cse2050.course_code} Roster Size: {len(cse2050.enrolled_roster)}")
    print(f"Course {cse2050.course_code} Waitlist Size: {len(cse2050.waitlist)}")
    print("")

    #Sorting
    print("Sorting (Merge Sort)")
    # Sort roster by Name using Merge Sort
    cse2050.enrolled_roster = merge_sort(cse2050.enrolled_roster, lambda x: x.student.name)
    print("Roster sorted by Student Name using Merge Sort.")
    print(f"Top 3 students: {[r.student.name for r in cse2050.enrolled_roster[:3]]}\n")

    # Binary Search and drop 
    print("Binary Search and drop ")
    # Sort by ID for Binary Search to work
    cse2050.enrolled_roster = quick_sort(cse2050.enrolled_roster, lambda x: x.student.student_id)
    target_id = cse2050.enrolled_roster[0].student.student_id
    
    print(f"Searching for {target_id} using Recursive Binary Search...")
    dropped_student = cse2050.drop(target_id)
    if dropped_student:
        print(f"Successfully dropped {dropped_student.name}. Waitlist promoted if available.")
    print("")
    print(f"Course {cse2050.course_code} Roster Size: {len(cse2050.enrolled_roster)}")
    print(f"Course {cse2050.course_code} Waitlist Size: {len(cse2050.waitlist)}")
    print("")

    # Undo functionality
    print("Undo functionality")
    undo_msg = cse2050.undo_action()
    print(f"Action undone: {undo_msg}")
    print(f"Course {cse2050.course_code} Roster Size: {len(cse2050.enrolled_roster)}")
    print(f"Course {cse2050.course_code} Waitlist Size: {len(cse2050.waitlist)}")
    print("")
    
    print("")
    print("            DEMO COMPLETE")
    print("-" * 50)
    

if __name__ == "__main__":
    run_milestone3_demo()