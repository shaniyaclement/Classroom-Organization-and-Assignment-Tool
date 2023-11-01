import csv

class Assignment:
    file_path = 'Classrooms_Demo.csv'
    with open(file_path, 'r', '') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
   
    # Initialize a dictionary to track classroom availability
    classroom_availability = {}
    for row in reader:
        classroom_name = row['Name']  # Name is in column 5
        classroom_availability[classroom_name] = {day: [] for day in ['M', 'T', 'W', 'TR', 'F']}
    #{"NEWLV 001": {'M': []}}
    
    # TODO: Assigns Course to a Classroom
    def assign_classroom(classroom_availability):
        file_path = 'Course_Catalog.csv'
        with open(file_path, 'r', '') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
        # for each line course read, implement logic to assign it to a classroom -- checks all classroom until it finds one that is available
        # access the course days, split it, loop through calling check_classroom_availibility to check it it is available for all needed days
        # call function that blocks the time out and call function if available for all days
        pass

    def check_classroom_availability(classroom_availability, start, end, day):
        # Iterate through the classrooms: key = room, value = availability
        for room, availability in classroom_availability.items():
            # Check if the day is in the availability dictionary.
            if day in availability:
                # Check if the room is available during the requested time range
                if is_room_available(availability[day], start, end):
                    # If the room is available, print a message indicating its availability and return true.
                    print(f"{room} is available on {day} from {start} to {end}")
                    return True

    # Check if a room is available during a specified time range
    def is_room_available(availability, start, end):
        # Iterate through the list of time frames for the room 
        for time in availability:  # time_frame is a tuple in availability, which is a list of tuples
            if start < time[1] and end > time[0]:
                # Check if there is overlap between the requested time and booked time
                return False
        # If no overlap is found, return True
        return True

    # TODO: implement a function that adds the tuple blocking that time off to the program
