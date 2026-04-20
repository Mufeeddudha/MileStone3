import statistics

GRADE_POINTS = {
'A' : 4.0, 'A-' : 3.7,
'B+': 3.3, 'B' : 3.0, 'B-' : 2.7,
'C+': 2.3, 'C' : 2.0, 'C-' : 1.7,
'D' : 1.0,
'F' : 0.0,
'N/A': 0.0
}

# Hashmap
class HashNode:
    """ Node for HashMap chaining
    Designed by: Mufeed Dudha"""
    def __init__(self, key, value):
        """Initialize a hash node with key, value, and next pointer."""
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    """ A simple HashMap implementation using chaining for collision resolution.
    Designed by: Mufeed Dudha"""
    def __init__(self, capacity=10):
        """Initialize a hash map with a specified capacity and empty buckets."""
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key):
        """Compute the hash value for a given key."""
        return hash(key) % self.capacity
    
    def put(self, key, value):
        """Insert or update a key-value pair in the hash map."""
        if self.size / self.capacity > 0.8:
            self.rehash()

        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = HashNode(key, value)
            self.size += 1
        else:
            curr = self.table[index]
            while curr:
                if curr.key == key:
                    curr.value = value
                    return
                if curr.next is None:
                    break
                curr = curr.next
            curr.next = HashNode(key, value)
            self.size += 1

    def get(self, key):
        """Retrieve the value associated with a given key."""
        index = self._hash(key)
        curr = self.table[index]

        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        return None

    def rehash(self):
        """Resize the hash table and rehash all existing key-value pairs."""
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            curr = node
            while curr:
                self.put(curr.key, curr.value)
                curr = curr.next


# Extra Credit: Stack For Undo
class StackNode:
    """ Node for LinkedStack
    Designed by: Marco Sileo Jr."""
    def __init__(self, data):
        """Initialize a stack node with data and next pointer."""
        self.data = data
        self.next = None

class LinkedStack:
    """ A stack implemented using a linked list.
    Designed by Marco Sileo Jr."""
    def __init__(self):
        """Initialize an empty stack with a top pointer and size."""
        self.top = None
        self._size = 0

    def push(self, item):
        """Adds an item to the top of the stack."""
        new_node = StackNode(item)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self):
        """Removes and returns the item at the top of the stack."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data
    
    def is_empty (self):
        """Returns True if the stack is empty, False otherwise."""
        return self.top is None



class Node:
    """
    Represents a node in a linked list.
    class designed by: Mufeed Dudha
    """
    def __init__(self, data):
        """Initialize a node with data and next pointer."""
        self.data = data
        self.next = None
# MileStone 2
class LinkedQueue:
    """
    A queue implemented using a linked list.
    Designed for Milestone 2: Waitlist implementation.
    Class designed by: Mufeed Dudha
    """
    def __init__(self):
        """ Initialize an empty queue with head, tail, and size."""
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, item):
        """Adds an item to the back (tail) of the queue."""
        new_node = Node(item)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def dequeue(self):
        """Removes and returns the item at the front (head) of the queue."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return data

    def is_empty(self):
        """Returns True if the queue is empty, False otherwise."""
        return self._size == 0

    def __len__(self):
        """Returns the current number of items in the queue."""
        return self._size






# MileStone 2
def recursive_binary_search(records, target_id, low, high):
    """Recursively searches for a student ID in a sorted list of EnrollmentRecord objects.
    Designed by: Mufeed Dudha"""
    if low > high:
        return -1
    mid = (low + high) // 2
    mid_id = records[mid].student.student_id
    
    if mid_id == target_id:
        return mid
    elif mid_id > target_id:
        return recursive_binary_search(records, target_id, low, mid - 1)
    else:
        return recursive_binary_search(records, target_id, mid + 1, high)

    


class EnrollmentRecord:

    """
    Represents an enrollment record with student and enrollment date.
    Designed by: Marco Sileo Jr.
    """
    def __init__(self, student, date):
        """Initialize an enrollment record with a student and enrollment date."""
        self.student = student
        self.date = date


class Course:
    """
    Represents a course and manages student enrollment.

    Class designed by: Marc Sileo Jr.
    """

    def __init__(self, course_code: str, credits: int, capacity: int = 100):
        """
        Initialize a Course object with course_code and # of credits
        """
        if not course_code:
            raise ValueError("Course code cannot be empty")

        if credits <= 0:
            raise ValueError("Credits must be positive")
        self.course_code = course_code
        self.credits = credits
        self.capacity = capacity
         

        self.prerequisite = None
        self.enrolled_roster = []
        self.waitlist = LinkedQueue()
        self.undo_stack = LinkedStack()
        self.sorted_by = None

        self.students = [] 

    def _sync_legacy_list(self):
        """Helper method to sync the legacy self.students list with the current enrolled_roster."""
        self.students = [record.student for record in self.enrolled_roster]

    # Waitlist and Enrollment
    def request_enroll(self, student, grade, enroll_date):
        """Attempts to enroll a student, pushing to waitlist if at capacity, adds them to the waitlist."""

        if self.prerequisite:
            """"""
            prev_grade = student.courses.get(self.prerequisite)

            if prev_grade is None:
                raise ValueError(f"Missing prerequisite: {self.prerequisite}")
            
            if prev_grade == 'F':
                raise ValueError(f"Failed prerequisite: {self.prerequisite}")
            
        if any(rec.student.student_id == student.student_id for rec in self.enrolled_roster):
            raise ValueError("Student is already enrolled.")
        
        new_record = EnrollmentRecord(student, enroll_date)
        if len(self.enrolled_roster) < self.capacity:
            self.enrolled_roster.append(new_record)
            student.courses[self.course_code] = grade
            self.undo_stack.push(("enroll", new_record))
            return f"{student.student_id} enrolled in {self.course_code}"
        else:
            self.waitlist.enqueue(new_record)
            self.undo_stack.push(("waitlist", new_record))
            return f"{student.student_id} added to waitlist for {self.course_code}"

        """for record in self.enrolled_roster:
            if record.student.student_id == student.student_id:
                raise ValueError("Student is already enrolled.")
            
        current = self.waitlist.head
        while current:
            waitlist_student = current.data[0]
            if waitlist_student.student_id == student.student_id:
                raise ValueError("Student is already on the waitlist.")
            current = current.next

        if len(self.enrolled_roster) < self.capacity:
            self.enrolled_roster.append(EnrollmentRecord(student, enroll_date))
            self.sorted_by = None
            self._sync_legacy_list()
            self.undo_stack.push(("enroll", student, grade, enroll_date))
            return True
        else:
            self.waitlist.enqueue((student, grade, enroll_date))
            self.undo_stack.push(("waitlist", student, grade, enroll_date)) 
            return False"""

    # EXTRA CREDIT 
    def undo_action(self):
        """Removes the last enrollment, waitlist addition, or drop from the course.
        Designed by: Mufeed Dudha
        """
        if self.undo_stack.is_empty():
            return "Nothing to Undo"
        
        
        action, student, grade, date = self.undo_stack.pop()

        if action == "enroll":
           
            self.enrolled_roster = [r for r in self.enrolled_roster if r.student.student_id != student.student_id]
            if self in student.courses: 
                del student.courses[self]

        elif action == "waitlist":
            
            if self.waitlist.is_empty():
                return "Waitlist already empty"
            
            
            temp_queue = LinkedQueue()
            while not self.waitlist.is_empty():
                item = self.waitlist.dequeue()
                
                if item[0].student_id != student.student_id:
                    temp_queue.enqueue(item)
            self.waitlist = temp_queue

        elif action == "drop":
            
            self.enrolled_roster.append(EnrollmentRecord(student, date))
            student.courses[self] = grade
            
            self.sorted_by = None

        self._sync_legacy_list()
        return f"Undid {action} for {student.name}"

    # Extra Credit
    def drop(self, student_id):
        """Drops a student using recursive binary search and records action for Undo.
        Designed by: Mufeed Dudha"""
        if self.sorted_by != 'id':
            self.sort_enrolled('id', 'insertion')
            
        index = recursive_binary_search(self.enrolled_roster, student_id, 0, len(self.enrolled_roster) - 1)

        if index == -1:
            raise ValueError("Student not found in enrolled roster.")

        
        record = self.enrolled_roster[index]
        student = record.student
        
        grade = student.courses.get(self, "N/A")
        date = record.date

        
        self.undo_stack.push(("drop", student, grade, date))

        
        dropped_record = self.enrolled_roster.pop(index)
        if self in student.courses:
            del student.courses[self]
        
        
        if not self.waitlist.is_empty():
            next_student, next_grade, next_date = self.waitlist.dequeue()
            self.enrolled_roster.append(EnrollmentRecord(next_student, next_date))
            next_student.courses[self] = next_grade
            self.sorted_by = None 

        self._sync_legacy_list()
        return dropped_record.student

    # Sorting
    def sort_enrolled(self, by, algorithm):
        """Sorts enrolled roster by name, id, or date using Insertion or Selection sort.
        Designed by: Marco Sileo Jr."""
        if by not in ['name', 'id', 'date']:
            raise ValueError("Invalid sort key. Choose 'name', 'id', or 'date'.")
            
        if algorithm not in ['insertion', 'selection']:
            raise ValueError("Invalid algorithm. Choose 'insertion' or 'selection'.")
        

        
        def get_key(record):
            """Helper function to extract the sorting key from an EnrollmentRecord."""
            if by == 'name': return record.student.name
            if by == 'id': return record.student.student_id
            if by == 'date': return record.date
            
        n = len(self.enrolled_roster)

        if n <= 1:
            self.sorted_by = by
            self._sync_legacy_list()
            return
    
        if algorithm == 'insertion':
            for i in range(1, n):
                key_item = self.enrolled_roster[i]
                j = i - 1
                while j >= 0 and get_key(self.enrolled_roster[j]) > get_key(key_item):
                    self.enrolled_roster[j + 1] = self.enrolled_roster[j]
                    j -= 1
                self.enrolled_roster[j + 1] = key_item
                
        elif algorithm == 'selection':
            for i in range(n):
                min_idx = i
                for j in range(i+1, n):
                    if get_key(self.enrolled_roster[j]) < get_key(self.enrolled_roster[min_idx]):
                        min_idx = j
                self.enrolled_roster[i], self.enrolled_roster[min_idx] = self.enrolled_roster[min_idx], self.enrolled_roster[i]
        else:
            raise ValueError("Unsupported algorithm. Choose 'insertion' or 'selection'.")
            
        self.sorted_by = by
        self._sync_legacy_list()


    def add_student(self, student):
        """
        Legacy method for Milestone 1 tests.
        """
        self.request_enroll(student, "A", "2024-01-01")

    def get_student_count(self):
        """
        Returns the number of students enrolled in that course.
        """
        return len(self.enrolled_roster)
    
class Student:
    """
    Represents a student and their course enrollments.

    Class designed by: Marc Sileo Jr.
    """
    def __init__(self, student_id: str, name: str):
        """
        Initialize a Student object with student_id, name, and courses.
        """
        if not student_id.startswith("STU") or len(student_id) != 8:
            raise ValueError("Invalid student ID")
        if not name:
            raise ValueError("Name cannot be empty")

        self.student_id = student_id
        self.name = name
        self.courses = {} 

    def enroll(self, course, grade, date):
        """
        Enrolls the student in a course with a specific grade and date.
        """
        if grade not in GRADE_POINTS:
            raise ValueError("Invalid grade")

        if course not in self.courses:
            enrolled = course.request_enroll(self, grade, date)
            
            if enrolled:
                self.courses[course] = grade

    def update_grade(self, course, grade):
        """
        Updates the student's grade for a course
        """
        if grade not in GRADE_POINTS:
            raise ValueError("Invalid grade")

        if course in self.courses:
            self.courses[course] = grade

    def calculate_gpa(self):
        """
        Calculates the student's GPA
        """
        total_points = 0
        total_credits = 0

        for course in self.courses:
            grade = self.courses[course]

            total_points += GRADE_POINTS[grade] * course.credits
            total_credits += course.credits

        if total_credits == 0:
            return 0.0

        return round(total_points / total_credits, 2)
    
    def get_courses(self):
        """
        Returns a list of courses the student is enrolled in.
        """
        return list(self.courses.keys())
    
    def get_course_info(self):
        """
        Returns a summary of all enrollments, including course code, grade,
        and credits.
        """
        info = []
        for course in self.courses:
            grade = self.courses[course]

            course_data = {}
            course_data["course_code"] = course.course_code
            course_data["grade"] = grade
            course_data["credits"] = course.credits

            info.append(course_data)

        return info
    
    def print_transcript(self):
        """Prints a transcript of the student's courses, grades, and GPA.
        Designed by: Mufeed Dudha"""
        print("\n======================================")
        print("Transcript")
        print("Name:", self.name)
        print("Student ID:", self.student_id)
        print("======================================")
        total_credits = 0

        for course in self.courses:
            grade = self.courses[course]
            print("Course:", course.course_code,
                  "| Grade:", grade,
                  "| Credits:", course.credits)
            total_credits += course.credits
        print("--------------------------------------")
        print("Total Credits:", total_credits)
        print("GPA:", self.calculate_gpa())
        print("======================================")

    
class University:
    """
    Represents a university and manages students and courses.

    Class designed by: Mufeed Dudha
    """
    def __init__(self):
        """ Initialize a University object with empty student and course"""
        self.students = {}
        self.courses = {}

    def add_course(self, course_code, credits, capacity=100):
        """
        Adds a course to the university's course catalog.
        """
        new_course = Course(course_code, credits, capacity)
        self.courses[course_code] = new_course
        return new_course
    
    def add_student(self, student_id, name):
        """
        Adds a student to the university's student registry.
        """
        new_student = Student(student_id, name)
        self.students[student_id] = new_student
        return new_student
        """if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
        return self.students[student_id]"""
    
    def get_student(self, student_id):
        """
        Gets the student object by their ID.
        """
        return self.students.get(student_id)
    
    def get_course(self, course_code):
        """
        Gets the course object by its code.
        """
        return self.courses.get(course_code)
    
    def get_course_enrollment(self, course_code):
        """
        Returns a list of students enrolled in a specific course.
        """
        course = self.get_course(course_code)
        return course.get_student_count() if course else 0
    
    def get_students_in_course(self, course_code):
        """
        Returns a list of student names enrolled in a specific course.
        """
        course = self.get_course(course_code)
        return course.students if course else []
    
    def get_gpa(self):
        """
        Returns mean, median, and mode of student GPAs.
        """
        gpas = [student.calculate_gpa() for student in self.students.values()]
        if not gpas:
            return None, None, None

        mean = round(statistics.mean(gpas), 2)
        median = round(statistics.median(gpas), 2)
        try:
            mode = round(statistics.mode(gpas), 2)
        except Exception:
            mode = round(max(gpas), 2)
        return mean, median, mode

    
    def get_course_stats(self, course_code):
        """
        Returns the mean, mode, and median for a course.
        """
        course = self.get_course(course_code)
        if not course or not course.students:
            return None, None, None
        
        points = [GRADE_POINTS[student.courses[course]] for student in course.students]
        mean = round(statistics.mean(points), 2)
        median = round(statistics.median(points), 2)
        mode = round(statistics.mode(points), 2)
        return mean, median, mode
    

    def get_common_students(self, course_code1, course_code2):
        """Return a set of student IDs enrolled in both courses."""
        c1 = self.get_course(course_code1)
        c2 = self.get_course(course_code2)
        if not c1 or not c2:
            return set()
        ids1 = {s.student_id for s in c1.students}
        ids2 = {s.student_id for s in c2.students}
        return ids1.intersection(ids2)


    def deans_list(self, threshold=3.5):
        """Returns a list of students with GPA above the threshold."""
    
        qualified = []

        for student in self.students.values():
            if student.calculate_gpa() >= threshold:
                qualified.append(student)

        return qualified
