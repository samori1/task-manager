# ========================== DATE TIME MODULE ==========================
from datetime import datetime

def validate_due_date(due_date_str):
    """
    Validate the due date to check if it is in the past and if the
    format is correct.
    Args:
    due_date_str (str): The due date as a string in 'day month year'
    format (e.g., '19 Oct 2019').
    Returns:
    str: A message indicating whether the due date is valid,
    in the past, or if the format is incorrect.
    """
    try:
        # Parse the due date from the string (format '19 Oct 2019')
        due_date = datetime.strptime(due_date_str, '%d %b %Y').date()
        today = datetime.today().date()

        # Check if due date is in the past
        if due_date < today:
            return "Warning: Due date is in the past"
        else:
            return "Due date is valid"
    except ValueError:
        return "Warning: Invalid date format, please use '19 Oct 2019'"

# ========================== DICTIONARIES AND FUNCTIONS ==========================

user_data = {}

MAX_USERNAME_LENGTH = 16
MAX_PASSWORD_LENGTH = 25

# Check the length of a username or password by using one of the indexes above.
def check_character_limit(username, max_length):
    try:
        _ = username[max_length]
        raise IndexError
    except IndexError:
        return len(username) <= max_length
    
# Request a username while using the character limit checker.
def username_check():
    while True:
        username = input("Enter username: ")
        if check_character_limit(username, MAX_USERNAME_LENGTH):
            return username
        else:
            print(f"Max character limit exceeded ({MAX_USERNAME_LENGTH})")

# Request a password while using the character limit checker.
def password_check():
    while True:
        password = input("Enter password: ")
        if check_character_limit(password, MAX_PASSWORD_LENGTH):
            return password
        else:
            print(f"Max character limit exceeded ({MAX_PASSWORD_LENGTH})")

# Store the existing users in a dictionary.
def download_user_data():
    try:
        with open(r'user.txt', 'r') as user_file:
            user_file.seek(0)
            for line in user_file.readlines():
                line = str(line).strip()
                if not line:
                    continue
                username, password = line.split(", ", 1)
                user_data[username] = password
        return ''
    except FileNotFoundError:
        return "Error: No user data has been found"

# Determine access by comparing new login with existing login details.
def read_logins(username, password):
    for validuser, validpassword in user_data.items():
        if validuser == username and validpassword == password:
            return f"\033[1mLogged in as {username}\033[0m\n"
    else:
            return "Error: Username or password invalid\n"
# ========================== LOG IN SECTION ==========================
logged_in = False
print("\033[1mWelcome\033[0m")
print(download_user_data())

while logged_in == False:
    ask_username = str(username_check())
    ask_password = str(password_check())
    check_login = read_logins(ask_username, ask_password)
    print(check_login)
    if (check_login) == f"\033[1mLogged in as {ask_username}\033[0m\n":
        logged_in = True

# =====================================================================
# Present the standard user menu.
while logged_in == True:
    if ask_username != "admin":
        menu = input('''Select one of the following options:
        a - add task
        va - view all tasks
        vm - view my tasks
        e - exit
        : ''').lower()
    # Present the admin user menu.
    # Only the admin can add users ('r') and read stats ('s').
    if ask_username == "admin":
        menu = input('''
        Please select one of the following options:
        r - register user
        a - add task
        va - view all tasks
        vm - view my tasks
        s - total number of tasks and users
        e - exit
        ''')

    if menu == 'r':
        new_username = username_check()
        if new_username in user_data:
            print("Error: username already registered\n")
        else:
            new_password = password_check()
            confirm = input("Confirm password: ")
            if confirm == new_password:
                user_data[f'{new_username}'] = new_password
                with open(r'user.txt', 'a') as user_file:
                    user_file.write(f'\n{new_username}, {new_password}')
                print(download_user_data())
                print("\033[1mNew user registered successfully\033[0m\n")
            else:
                print("Error: new login details do not match\n")
    
    elif menu == 's':
        print("\nUsers:")
        print(len(user_data))
        print("\nTasks:")
        with open(r"tasks.txt", "r") as task_file:
            information = task_file.readlines()
            print(len(information))
    # Add and assign a task to an availible user.
    elif menu == 'a':
        new_task_user = input("Enter the user assigned to the task: ")
        if new_task_user not in user_data:
            print("Error: this user is not registered\n")
        else: 
            new_task_name = input("Enter the name of the task: ")
            new_task_descript = input("Enter the desription of the task: ")
            today_date = input("Enter today's date e.g. 19 Oct 2019: ")
            due_date = input("Enter the end date of the task e.g. 19 Oct 2019: ")
            date_validation = validate_due_date(due_date)
            print(date_validation)
            completion = input("Enter the task completion status e.g. Yes: ")
            with open(r'tasks.txt', 'a') as task_file:
                task_file.write(f'\n{new_task_user}, {new_task_name}, '
                                f'{new_task_descript}, {today_date}, '
                                f'{due_date}, {completion}')
            print("\033[1mNew task added successfully\033[0m\n")
    # View all outstanding tasks in the task manager system.
    elif menu == 'va':
        with open(r"tasks.txt", "r") as task_file:
            information = task_file.readlines()
            for task in information:
                parts = task.split(", ")
                user = parts[0]
                task_info = parts[1:6]
                readable_task_info = [item.strip() for item in task_info]
                print(f"\033[1m{user}\033[0m" + f"\n{", ".join(readable_task_info)}")
                print()
    # View the logged in user's task only.
    elif menu == 'vm':
        with open(r"tasks.txt", "r") as task_file:
            information = task_file.readlines()
            counter = 0
            for task in information:
                parts = task.split(", ")
                user = parts[0]
                task_info = parts[1:6]
                readable_task_info = [item.strip() for item in task_info]
                if str(user) == ask_username:
                    print(f"\033[1m{user}\033[0m" + f"\n{", ".join(readable_task_info)}")
                    print()
                    counter += 1
            if counter == 0:
                print("Error: no tasks found for this user\n")

    # Log off.
    elif menu == 'e':
        print("\033[1mGoodbye\033[0m\n")
        exit()
    else:
        print("Invalid input\n")