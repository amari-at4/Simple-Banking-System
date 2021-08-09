students_first_group = abs(int(input()))
students_second_group = abs(int(input()))
students_third_group = abs(int(input()))

desks_first_group = (students_first_group // 2) + (students_first_group % 2)
desks_second_group = (students_second_group // 2) + (students_second_group % 2)
desks_third_group = (students_third_group // 2) + (students_third_group % 2)

print(desks_first_group + desks_second_group + desks_third_group)
