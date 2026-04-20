import unittest
from classes import HashMap, University

class TestPrereqEnrollment(unittest.TestCase):
    """Test enrollment in courses with prerequisites.
    Designed by: Mufeed Dudha"""
    def setUp(self):
        self.uni = University()
        # Setup: CSE1010 (No prereq), CSE2050 (Prereq: CSE1010)
        self.c1 = self.uni.add_course("CSE1010", 3, 10)
        self.c2 = self.uni.add_course("CSE2050", 3, 10)
        self.c2.prerequisite = "CSE1010"
        
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

    def test_enroll_failed_prereq(self):
        """Should fail: Student took CSE1010 but failed it."""
        
        self.student.courses["CSE1010"] = "F"
        with self.assertRaises(ValueError) as cm:
            self.c2.request_enroll(self.student, "N/A", "2026-01-01")
        self.assertIn("Failed prerequisite", str(cm.exception))

    def test_enroll_with_valid_prereq(self):
        """Should succeed: Student passed CSE1010 with a B."""
        self.student.courses["CSE1010"] = "B"
        msg = self.c2.request_enroll(self.student, "N/A", "2026-01-01")
        self.assertIn("enrolled", msg)

class TestHashMap(unittest.TestCase):
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
