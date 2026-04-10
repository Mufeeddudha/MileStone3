import unittest
from classes import HashMap

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
