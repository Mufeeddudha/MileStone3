import unittest
from classes import HashMap, University


class TestSorting(unittest.TestCase):
    def setUp(self):
        """Set up a university and a course with students for sorting tests.
        Designed by: Mufeed Dudha"""
        self.uni = University()
        self.course = self.uni.add_course("CSE1010", 3, 10)
        
        # Create students with ids and names
        s1 = self.uni.add_student("STU00001", "Zebra")
        s2 = self.uni.add_student("STU00002", "Apple")
        s3 = self.uni.add_student("STU00003", "Middly")
        
        #
        # Zebra (STU00001) -> Feb | Apple (STU00002) -> Jan | Middly (STU00003) -> Mar
        self.course.request_enroll(s1, "N/A", "2026-02-01")
        self.course.request_enroll(s2, "N/A", "2026-01-01")
        self.course.request_enroll(s3, "N/A", "2026-03-01")

    # Merge sort
    def test_merge_sort_by_id(self):
        """Test merge sort of enrolled roster by student ID."""
        from classes import merge_sort
        sorted_roster = merge_sort(self.course.enrolled_roster, lambda x: x.student.student_id)
        ids = [r.student.student_id for r in sorted_roster]
        self.assertEqual(ids, ["STU00001", "STU00002", "STU00003"])

    def test_merge_sort_by_name(self):
        """Test merge sort of enrolled roster by student name."""
        from classes import merge_sort
        sorted_roster = merge_sort(self.course.enrolled_roster, lambda x: x.student.name)
        names = [r.student.name for r in sorted_roster]
        self.assertEqual(names, ["Apple", "Middly", "Zebra"])

    def test_merge_sort_by_date(self):
        """Test merge sort of enrolled roster by enrollment date."""
        from classes import merge_sort
        sorted_roster = merge_sort(self.course.enrolled_roster, lambda x: x.date)
        dates = [r.date for r in sorted_roster]
        self.assertEqual(dates, ["2026-01-01", "2026-02-01", "2026-03-01"])

    # quick sort
    def test_quick_sort_by_id(self):
        """Test quick sort of enrolled roster by student ID."""
        from classes import quick_sort
        sorted_roster = quick_sort(self.course.enrolled_roster, lambda x: x.student.student_id)
        ids = [r.student.student_id for r in sorted_roster]
        self.assertEqual(ids, ["STU00001", "STU00002", "STU00003"])

    def test_quick_sort_by_name(self):
        """Test quick sort of enrolled roster by student name."""
        from classes import quick_sort
        sorted_roster = quick_sort(self.course.enrolled_roster, lambda x: x.student.name)
        names = [r.student.name for r in sorted_roster]
        self.assertEqual(names, ["Apple", "Middly", "Zebra"])

    def test_quick_sort_by_date(self):
        """Test quick sort of enrolled roster by enrollment date."""
        from classes import quick_sort
        sorted_roster = quick_sort(self.course.enrolled_roster, lambda x: x.date)
        dates = [r.date for r in sorted_roster]
        self.assertEqual(dates, ["2026-01-01", "2026-02-01", "2026-03-01"])

class TestPrereqEnrollment(unittest.TestCase):
    """Test enrollment in courses with prerequisites.
    Designed by: Mufeed Dudha"""
    def setUp(self):
        self.uni = University()
        # Setup: CSE1010 (No prereq), CSE2050 (Prereq: CSE1010) 
        self.c1 = self.uni.add_course("CSE1010", 3, 10)
        self.c2 = self.uni.add_course("CSE2050", 3, 10)
        self.c2.prerequisite.put("CSE1010", True)
        
        self.student = self.uni.add_student("STU00001", "Test Student")

    def test_enroll_no_prereq(self):
        """Should succeed: CSE1010 has no prerequisites."""
        msg = self.c1.request_enroll(self.student, "N/A", "2026-01-01")
        self.assertIn("enrolled", msg)

    def test_enroll_missing_prereq(self):
        """Should fail: Student has not taken CSE1010 yet."""
        with self.assertRaises(ValueError) as cm:
            self.c2.request_enroll(self.student, "N/A", "2026-01-01")
        self.assertIn("Missing prerequisite", str(cm.exception))


    def test_enroll_with_valid_prereq(self):
        """Should succeed: Student passed CSE1010 with a B."""
        self.student.courses["CSE1010"] = "B"
        msg = self.c2.request_enroll(self.student, "N/A", "2026-01-01")
        self.assertIn("enrolled", msg)

class TestHashMap(unittest.TestCase):
    """Test the custom HashMap implementation.
    Designed by: Mufeed Dudha"""
    def setUp(self):
        """Set up a new HashMap instance before each test.
        """
        self.h = HashMap(capacity=5)

    def test_basic_put_get(self):
        """Test basic put and get operations."""
        self.h.put("CSE1010", "Intro to Computing")
        self.assertEqual(self.h.get("CSE1010"), "Intro to Computing")

    def test_update_value(self):
        """Test updating the value of an existing key."""
        self.h.put("Key1", "Value1")
        self.h.put("Key1", "UpdatedValue1")
        self.assertEqual(self.h.get("Key1"), "UpdatedValue1")

    def test_collisons(self):
        """Test handling of collisions."""
        
        self.h.put("A", "1")
        self.h.put("B", "2")  
        self.h.put("C", "3")
        self.assertEqual(self.h.get("A"), "1")
        self.assertEqual(self.h.get("B"), "2")
        self.assertEqual(self.h.get("C"), "3")

    def test_rehasing(self):
        """Test that the HashMap resizes correctly."""
        initial_cap = self.h.capacity
        for i in range(10):
            self.h.put(f"Key{i}", i)
        
        self.assertGreater(self.h.capacity, initial_cap)
        self.assertEqual(self.h.get("Key9"), 9)
    
    def test_missing_key(self):
        """Test that getting a missing key raises KeyError."""
        self.assertIsNone(self.h.get("GhostKey"))

if __name__ == "__main__":
    unittest.main()
