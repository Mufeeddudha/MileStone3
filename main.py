import csv

from classes import University
from loader import load_courses, load_students, load_prerequisites

uni = University()
load_courses("course_catalog_CSE10_with_capacity.csv", uni)
load_students("enrollments_CSE10.csv", uni)
load_prerequisites("cse_prerequisites.csv", uni)

from demo_milestone3 import run_milestone3_demo

# Uncomment the lines below to run the demo
#if __name__ == "__main__":
    #run_milestone3_demo()

