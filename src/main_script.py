import functions as my_fun

default_name = "poppiepayne"
default_pass = "456827913"

my_target = str(input("Profile you want to analyze: "))
print("You have selected profile handle: " + my_target)
my_login = str(input("Profile you want to login with: "))
print("You have selected to login as: " + my_login)
my_start = str(input("Start date (YYYY-MM_DD), don't enter anything for default: "))
print("You have selected start date: " + my_start)
my_end = str(input("End date (YYYY-MM_DD), don't enter anything for default: "))
print("You have selected start date: " + my_end)

my_fun.get_data(target_name = my_target, login_name = my_login)
my_fun.analyze_data(target_name = my_target, from_date = my_start, to_date= my_end)

print('Done!')