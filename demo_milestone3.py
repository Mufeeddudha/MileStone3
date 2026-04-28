from classes import University, merge_sort, quick_sort, recursive_binary_search
from loader import load_courses, load_students, load_prerequisites

def run_milestone3_demo():
    print("==========================================")
    print("   UNIVERSITY SYSTEM MILESTONE 3 DEMO")
    print("        Designed by: Mufeed Dudha")
    print("==========================================\n")

    uni = University()

    # --- STEP 1: LOADING DATA (Milestones 1, 2, & 3) ---
    print("--- Step 1: Loading Data Structures ---")
    load_courses("course_catalog_CSE10_with_capacity.csv", uni)
    load_students("enrollments_CSE10.csv", uni)
    load_prerequisites("cse_prerequisites.csv", uni)
    print("Successfully loaded Courses, Students, and Prerequisites into HashMaps.\n")

    # --- STEP 2: HASHMAP LOOKUP (Milestone 3) ---
    print("--- Step 2: Custom HashMap Verification ---")
    test_student_id = "STU00164"
    # Demonstrating the use of your custom .get() method
    student = uni.students.get(test_student_id)
    if student:
        print(f"HashMap Lookup Success: Found {student.name} ({student.student_id})")
    print("")

    # --- STEP 3: PREREQUISITE CHECKS (Milestone 3 Lab) ---
    print("--- Step 3: Prerequisite Enrollment Logic ---")
    cse2050 = uni.get_course("CSE2050") # Has prereq: CSE1010
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

    # --- STEP 4: WAITLIST LOGIC (Milestone 2) ---
    print("--- Step 4: Waitlist & Capacity Management ---")
    cse1010 = uni.get_course("CSE1010")
    print(f"Course {cse1010.course_code} Roster Size: {len(cse1010.enrolled_roster)}")
    print(f"Course {cse1010.course_code} Waitlist Size: {len(cse1010.waitlist)}")
    print("")

    # --- STEP 5: LOGARITHMIC SORTING (Milestone 3) ---
    print("--- Step 5: O(n log n) Sorting (Merge Sort) ---")
    # Sort roster by Name using Merge Sort
    cse1010.enrolled_roster = merge_sort(cse1010.enrolled_roster, lambda x: x.student.name)
    print("Roster sorted by Student Name using Merge Sort.")
    print(f"Top 3 students: {[r.student.name for r in cse1010.enrolled_roster[:3]]}\n")

    # --- STEP 6: BINARY SEARCH & DROP (Milestone 2) ---
    print("--- Step 6: Binary Search & Student Drop ---")
    # Must sort by ID for Binary Search to work
    cse1010.enrolled_roster = quick_sort(cse1010.enrolled_roster, lambda x: x.student.student_id)
    target_id = cse1010.enrolled_roster[5].student.student_id
    
    print(f"Searching for {target_id} using Recursive Binary Search...")
    dropped_student = cse1010.drop(target_id)
    if dropped_student:
        print(f"Successfully dropped {dropped_student.name}. Waitlist promoted if available.")
    print("")

    # --- STEP 7: UNDO ACTION (Extra Credit) ---
    print("--- Step 7: Extra Credit Undo ---")
    undo_msg = cse1010.undo_action()
    print(f"Action undone: {undo_msg}")
    print("==========================================")
    print("            DEMO COMPLETE")
    print("==========================================")

if __name__ == "__main__":
    run_milestone3_demo()