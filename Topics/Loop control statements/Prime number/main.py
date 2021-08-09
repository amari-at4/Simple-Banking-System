number = int(input())

times_divisible = 0
for _i in range(1, number + 1):
    if number % _i == 0:
        times_divisible += 1

if times_divisible == 2:
    print("This number is prime")
else:
    print("This number is not prime")
