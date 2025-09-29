import numpy as np
import random

# 三门问题：

times = 1000000

correct_times_before_change = 0

correct_times_after_change = 0

for i in range(0, times):
    car_location = random.randint(0,2)

    selected = random.randint(0,2)

    goats = set([0,1,2]) - set([car_location])

    random_goat = random.choice(list(goats))

    the_other_choice = list(set([0,1,2]) - set([selected]) - set([random_goat]))

    if selected == car_location:
        correct_times_before_change = correct_times_before_change + 1
    if the_other_choice[0] == car_location:
        correct_times_after_change = correct_times_after_change + 1

print("Winning rate before changed: " + str(correct_times_before_change / times))
print("Winning rate after changed: " + str(correct_times_after_change / times))
