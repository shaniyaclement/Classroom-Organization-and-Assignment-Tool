import os
import csv
from datetime import datetime

class Assignment:
    classrooms = 'Classrooms.csv'
    course_catalog = 'Course_Catalog.csv'
    assigned_courses = 'Assigned_Courses.csv'
    conflicting_courses = 'Conflicting_Courses.csv'
    online_course = ['Main','Online','ONL',',','Online','Online','Online','Online',',']
    assigned_buildngs = {'ACC': ['PARKJ'], 'ART': ['JUBL'], 'BAD': ['PARKJ'], 'CSCI': ['SCILB']}

    # Initialize a dictionary to track classroom availability
    def assign_availability(classrooms):
        classroom_availability = {}
        classrooms = classrooms
        with open(classrooms, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                classroom_name = row[4]  # Name is in column 5
                classroom_availability[classroom_name] = {day: [] for day in ['M', 'T', 'W', 'TR', 'F']}
                classroom_availability[classroom_name]['info'] = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]]
        return classroom_availability
    
    # Turns string of course days into list where TR is represented as one day
    def split_days_string(course_days):
        course_days_split = []
        i = 0
        while i < len(course_days):
            current_char = course_days[i]
            course_days_split.append(current_char)
            if current_char == 'T' and i + 1 < len(course_days) and course_days[i + 1] == 'R':
                course_days_split[-1] = 'TR'
                i += 1 
            i += 1
        return course_days_split
    
    def check_classroom_availability(classroom, department, course_start, course_end, course_days, course_capacity):
        # Check if course capacity exceeds the room capacity
        if (int(course_capacity) > int(classroom['info'][9])):
            print(f"Exceeds capacity: {course_capacity} > {classroom['info'][9]}")
            return False
        elif department in Assignment.assigned_buildngs:
            if classroom['info'][2] not in Assignment.assigned_buildngs[department]:
                print(classroom['info'][2], Assignment.assigned_buildngs[department])
                return False
        new_interval = (course_start, course_end)
        for day in course_days:
            for course_time in classroom[day]:
                existing_interval = (course_time[0], course_time[1])
                if not (new_interval[1] <= existing_interval[0] or new_interval[0] >= existing_interval[1]):
                    print(f"Overlap found: {classroom['info'][4]} is not available on {day} from {course_start} to {course_end}.")
                    return False  # Overlap found
        return True  # No overlap, classroom available on each needed day    

    def add_course(classroom, course, course_start, course_end, course_days):
        if 'ONL' not in course[1]:
            new_interval = (course_start, course_end)
            for day in course_days:
                classroom[day].append(new_interval)
        course = ','.join(course)
        classroom = ','.join(classroom['info'])

        # Check if the CSV file exists
        if not os.path.exists(Assignment.assigned_courses):
            # Read header from Course_Catalog.csv
            with open(Assignment.course_catalog, 'r') as file:
                course_header = file.readline().strip()  # strip() removes leading/trailing whitespaces
            # Read headers from Classrooms_Demo.csv
            with open(Assignment.classrooms, 'r') as file:
                classroom_header = file.readline().strip()
            # Combine headers
            header = course_header + ',' + classroom_header

            with open(Assignment.assigned_courses, 'w') as csv_file:
                csv_file.write(header + '\n')  # Write the header

        # Add a course to the end of the CSV file
        with open(Assignment.assigned_courses, 'a') as csv_file:
            csv_file.write(course + ',' + classroom + '\n')

    def conflicts(course):
        course = ','.join(course)

        # Check if the CSV file exists
        if not os.path.exists(Assignment.conflicting_courses):
            # Read header from Course_Catalog.csv
            with open(Assignment.course_catalog, 'r') as file:
                header = file.readline().strip()
            with open(Assignment.conflicting_courses, 'w') as csv_file:
                csv_file.write(header + '\n')  # Write the header

        # Add course to the end of the CSV file
        with open(Assignment.conflicting_courses, 'a') as csv_file:
            csv_file.write(course + '\n')

    def assign_classroom():
        classroom_availability = Assignment.assign_availability(Assignment.classrooms)
        # Read the course catalog
        file_path = Assignment.course_catalog
        with open(file_path, 'r') as file:
            course_reader = csv.reader(file)
            next(course_reader) # Skip the header row
            for course in course_reader:
                # Split the course days so it's easier to check for each day
                department = course[0]
                course_id = course[1]
                course_name = course[2]
                course_days = Assignment.split_days_string(course[3])
                # Convert strings to time objects
                course_start = datetime.strptime(course[4], '%H%M').time()
                course_end = datetime.strptime(course[5], '%H%M').time()
                course_capacity = course[6]
                course = [department, course_id, course_name, course[3], course[4], course[5], course_capacity]
                
                # Online courses do not need room assignments 
                if 'ONL' in course_id:
                    print("ONL course")
                    Assignment.add_course({'info': Assignment.online_course}, course, course_start, course_end, course_days)
                else:
                    print(course_name)
                    # while loop somewhere
                    for classroom in classroom_availability:
                        available = Assignment.check_classroom_availability(classroom_availability[classroom], department, course_start, course_end, course_days, course_capacity)
                        if available == True:
                            Assignment.add_course(classroom_availability[classroom], course, course_start, course_end, course_days)
                            break
                    if available == False:
                        Assignment.conflicts(course)
