import unittest
from classes import University, Student, Course, LinkedQueue, recursive_binary_search, EnrollmentRecord

class TestMilestone2(unittest.TestCase):
    def setUp(self):
        """Initializes a fresh university environment for every test.
        Used from external resource (https://docs.python.org/3/library/unittest.html) 
        Class designed by Mufeed Dudha 
        """
        self.uni = University()
        
        self.course = self.uni.add_course("CSE10", credits=3, capacity=2)
        self.s1 = self.uni.add_student("STU00001", "Alice")
        self.s2 = self.uni.add_student("STU00002", "Bob")
        self.s3 = self.uni.add_student("STU00003", "Charlie")

    # LinkedQueue
    def test_queue_behavior(self):
        """FIFO order and empty queue error handling."""
        q = LinkedQueue()
        q.enqueue("First")
        q.enqueue("Second")
        self.assertEqual(q.dequeue(), "First")
        self.assertEqual(len(q), 1)
        q.dequeue()
        with self.assertRaises(IndexError):
            q.dequeue()

    # Enrollment & Waitlist 
    def test_enrollment_and_waitlist(self):
        """Capacity limits and waitlist functionality."""
        self.s1.enroll(self.course, "A", "2026-01-01")
        self.s2.enroll(self.course, "B", "2026-01-02")
        
        enrolled_success = self.s3.enroll(self.course, "A", "2026-01-03")
        
        self.assertFalse(enrolled_success) 
        self.assertEqual(self.course.get_student_count(), 2)
        self.assertEqual(len(self.course.waitlist), 1)

    def test_drop_and_promotion(self):
        """Dropping a student promotes the next person from waitlist."""
        self.s1.enroll(self.course, "A", "2026-01-01")
        self.s2.enroll(self.course, "B", "2026-01-02")
        self.s3.enroll(self.course, "A", "2026-01-03") 
        
        self.course.drop("STU00001") 
        self.assertEqual(self.course.enrolled_roster[-1].student.name, "Charlie")
        self.assertEqual(len(self.course.waitlist), 0)

    # Sorting
    def test_sorting_logic(self):
        """Roster sorting by ID and Name."""
        self.s1.enroll(self.course, "A", "2026-01-01") 
        self.s2.enroll(self.course, "A", "2026-01-01") 
        
        
        self.course.sort_enrolled(by='name', algorithm='insertion')
        self.assertEqual(self.course.enrolled_roster[0].student.name, "Alice")

        
        self.course.sort_enrolled(by='id', algorithm='selection')
        self.assertEqual(self.course.enrolled_roster[0].student.student_id, "STU00001")

    # Recursive Binary Search
    def test_binary_search(self):
        """Recursive binary search for student IDs."""
        self.s1.enroll(self.course, "A", "2026-01-01")
        self.s2.enroll(self.course, "B", "2026-01-02")
        
        
        self.course.sort_enrolled(by='id', algorithm='insertion')
        
        idx = recursive_binary_search(self.course.enrolled_roster, "STU00002", 0, 1)
        self.assertEqual(idx, 1)

    # Extra Credit: Duplicates & Undo
    def test_duplicate_prevention(self):
        """Extra Credit: Ensure ValueError is raised for duplicate enrollment."""
        self.s1.enroll(self.course, "A", "2026-01-01")
        with self.assertRaises(ValueError):
            self.course.request_enroll(self.s1, "A", "2026-01-01")

    def test_undo_action(self):
        """Extra Credit: Verify Stack-based undo removes last enrollment."""
        self.s1.enroll(self.course, "A", "2026-01-01")
        self.assertEqual(self.course.get_student_count(), 1)
        
        self.course.undo_action()
        self.assertEqual(self.course.get_student_count(), 0)

if __name__ == "__main__":
    unittest.main()