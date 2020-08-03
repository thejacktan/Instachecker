import functions as my_fun

# Default username and password for throw-away account
default_name = "poppiepayne"
default_pass = "456827913"

my_target = str(input("Profile you want to analyze: "))
print("You have selected profile handle: " + my_target)
my_login = str(input("Profile you want to login with (leave blank for default): "))

if len(my_login) == 0:
    my_login = default_name
    my_pass = default_pass
else:
    my_pass = str(input("Password for " + my_login + " : "))

my_start = str(input("Start date (YYYY-MM-DD), leave blank for default: "))
my_end = str(input("End date (YYYY-MM-DD), leave blank for default: "))

# Input arguments into functions
my_fun.get_data(target_name=my_target, login_name=my_login, login_pass=my_pass)
my_fun.analyze_data(target_name=my_target, from_date=my_start, to_date=my_end)

print('Done!')
