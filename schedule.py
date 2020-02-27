#Source for this exercise:
#https://www.youtube.com/watch?v=3Q_oYDQ2whs&feature=youtu.be
#https://www.reddit.com/r/learnpython/comments/fa00ck/my_take_on_a_google_interview/

#INPUT DATA
person1_schedule = [['09:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
person1_bounds = ['09:00', '20:00']

person2_schedule = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
person2_bounds = ['10:00', '18:30']

meeting_time = 30
#list representing all the minutes in a day, initially set to 0 for 'unavailable'
min_in_day = [0 for _ in range(0, 1440)]

#list with times where both persons are free to meet
shared_times = []

#time_to_mins takes in a list with two string values representing a start and endtime e.g. ['10:00', '12:00']
#it returns a range in minutes
def time_to_mins(list_with_times):
    start_hour, start_min = list_with_times[0].split(':')
    end_hour, end_min = list_with_times[1].split(':')
    start_time = int(start_hour)*60+int(start_min)
    end_time = int(end_hour)*60+int(end_min)
    return range(start_time, end_time)

#mins_to_time is the reverse of time_to_mins, it takes in a list of 2 integer values representing minutes e.g. [0, 60]
#it returns a list of strings e.g. ['00:00', '01:00']
def mins_to_time(list_with_mins):
    start_hour, start_min = divmod(list_with_mins[0], 60)
    end_hour, end_min = divmod(list_with_mins[1], 60)
    return [f'{start_hour:02d}:{start_min:02d}', f'{end_hour:02d}:{end_min:02d}']


#bounds in military time are converted to ranges in minutes
person1_bounds_min = time_to_mins(person1_bounds)
person2_bounds_min = time_to_mins(person2_bounds)

#first set each person's availability to within the bounds
person1_available = [1 if i in person1_bounds_min else 0 for i, _ in enumerate(min_in_day) ]
person2_available = [1 if i in person2_bounds_min else 0 for i, _ in enumerate(min_in_day) ]

#second, set each persons unavailability – can be done better I suspect. Up for refactoring!
for unavailable in person1_schedule:
    unavailable = time_to_mins(unavailable)
    for i in unavailable:
        person1_available[i] = 0

for unavailable in person2_schedule:
    unavailable = time_to_mins(unavailable)
    for i in unavailable:
        person2_available[i] = 0

#multiply the lists of each person. Only minutes where both are available will be set to 1
common_availability = [a * b for a, b in zip(person1_available, person2_available)]


#This needs some more work...but it works:
#go through the list common_availability and take out all the consecutive chunks where both persons are available
#add them to the list shared_times which will end up containing all the possible timeslots for a meeting that fulfill
#the requirement of minimum meeting time length.

start = 0
end = 0
i = 0
while i < len(common_availability):
        end = i
        while all(common_availability[i:end]) and end < len(common_availability):
            end += 1
        if len(common_availability[i:end-1]) > 0 and (end-1 - i) >= meeting_time:
            shared_times.append([i, end-1])
        i = end


print([mins_to_time(times) for times in shared_times])
