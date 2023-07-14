# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date
from collections import defaultdict

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", "r") as task_file:
    task_data = task_file.read().split("\n")
    print(task_data)
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t["username"] = task_components[0]
    curr_t["title"] = task_components[1]
    curr_t["description"] = task_components[2]
    curr_t["due_date"] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t["assigned_date"] = datetime.strptime(
        task_components[4], DATETIME_STRING_FORMAT
    )
    curr_t["completed"] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


# ====Login Section====
"""This code reads usernames and password from the user.txt file to 
    allow a user to login.
"""
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", "r") as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(";")
    username_password[username] = password

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


def reg_user():
    """Add a new user to the user.txt file"""
    uniqueName = False

    # This will check to see if a new username is being added or if it exists
    while uniqueName == False:
        try:
            new_username = input("New Username: ")
            if new_username in username_password.keys():
                print("Username already taken. Please try again.")
            else:
                uniqueName = True
        except ValueError:
            print("Invalid input. Please try again.")

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        #If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    #Otherwise you present a relevant message.
    else:
        print("Passwords do not match")


def add_task():
    while True:
        try:
            # We must make sure that the user you assign a task to is in the key list
            task_username = input("Name of person assigned to task: ")
            if task_username not in username_password.keys():
                print("User does not exist. Please enter a valid username")
                return  # same as continue but for functions instead, it will return nothing here and ignore the rest of the code below.
            break
        except ValueError:
            print("Invalid input. Please try again.")

    # Add the title and description
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            # Add the due date 
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    """ Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete."""
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False,
    }

    # Updates the tasks in the tasks.txt file
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t["username"],
                t["title"],
                t["description"],
                t["due_date"].strftime(DATETIME_STRING_FORMAT),
                t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t["completed"] else "No",
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all():
    """Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    """

    # Loops through the tasks list to print out all tasks
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += (
            f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        )
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        
        print(disp_str)


def view_mine():
    task_dict = {}

    print("* * * * * * * * * * * * * * * * * * * * * * * * * * *")

    task_num = 0
    for t in task_list:
        # Checks what user to display the information for
        if t["username"] == curr_user:
            # Will dispaly what task number it is for the user
            task_num += 1  # task_num = task_num + 1
            task_dict[task_num] = t

            # Prints the users task information
            print("                       Task ", task_num)
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += (
                f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            )
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Completed: \t {t['completed']}\n"
            print(disp_str)
            print("* * * * * * * * * * * * * * * * * * * * * * * * * * *")

    # If the user has no tasks then a message will be displayed 
    if task_num == 0:
        print("\t\t This user has no tasks")
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * *")
        return

    # Checks what the user would like to do with the tasks
    while True:
        try:
            user_input = int(
                input(
                    "Which task would you like to view? (Press -1 to return to menu)\n: "
                )
            )
            # Allows the user to return to the menu
            if user_input == -1:
                return
            elif user_input > 0 and user_input <= task_num:
                break
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer")

    selected_task = task_dict[user_input]

    # Re-displays the users task information
    print("\n                       Task ", user_input)
    disp_str = f"Task: \t\t {selected_task['title']}\n"
    disp_str += f"Assigned to: \t {selected_task['username']}\n"
    disp_str += f"Date Assigned: \t {selected_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += (
        f"Due Date: \t {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    )
    disp_str += f"Task Description: \n {selected_task['description']}\n"
    disp_str += f"Completed: \t {selected_task['completed']}\n"
    print(disp_str)

    # Will not allow users to edit completed tasks
    if selected_task["completed"] == True:
        print("Task already complete. Unable to edit.")
        return
    else:
        print(
            "Options for selected task\n1. Mark task as complete\n2. Edit due date of task\n3. Edit the user task is assigned to\n\n(Press -1 to return to menu)"
        )

    while True:
        try:
            edit_input = int(input(": "))
            if edit_input == -1:
                return
            elif edit_input >= 1 and edit_input <= 3:
                break
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer")

    # Changes incomplete files to complete if incomplete
    if edit_input == 1:
        selected_task["completed"] = True
        print("Task succesfully marked as complete.")

    elif edit_input == 2:
        while True:
            try:
                date_entry = input("Please enter a date in YYYY-MM-DD format: ")
                year, month, day = map(int, date_entry.split("-"))
                new_date = datetime(year, month, day)

                if new_date < selected_task["assigned_date"]:  # bad case
                    print(
                        "Invalid date. Due date cannot be before assigned date. Please try again.\n"
                    )
                else:  # good case
                    selected_task["due_date"] = new_date
                    print(
                        "Due date successfully changed. New due date is ",
                        new_date.strftime(DATETIME_STRING_FORMAT),
                    )
                    break
            except ValueError:
                print("Invalid date format. Please try again.")

    # Allows the user to change who the task is assigned to
    elif edit_input == 3:
        while True:
            try:
                new_user = input(
                    "Please enter the user you wish to assign the task to: "
                )  
                if new_user not in username_password.keys():
                    print("Invalid user. Please try again")
                else:
                    selected_task["username"] = new_user
                    print(
                        "User assigned to succesfully changed. New user is ", new_user
                    )
                    break
            except ValueError:
                print("Invalid input. Please try again.)")

    # Saves changes to the tasks.txt file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t["username"],
                t["title"],
                t["description"],
                t["due_date"].strftime(DATETIME_STRING_FORMAT),
                t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t["completed"] else "No",
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("\nTask successfully updated.")

    """
    
    str_attrs = ["admin","Add functionality to task manager","Add additional options and refactor the code.","2022-12-01","2022-11-22","No"]
    str_attrs_joined = "admin;Add functionality to task manager;Add additional options and refactor the code.;2022-12-01;2022-11-22;No"
    task_list_to_write = ["admin;Add functionality to task manager;Add additional options and refactor the code.;2022-12-01;2022-11-22;No","admin2;Add functionality to task manager;Add additional options and refactor the code.;2022-12-01;2022-11-22;No","admin;Add functionality to task manager;Add additional options and refactor the code.;2023-06-06;2022-11-22;Yes"]
    for every line in task_list_to_write:
    write to file(line)

    """


def generate_reports():
    # Creating the task overview file
    with open("task_overview.txt", "w") as file:
        # Task counters
        num_tasks = len(task_list)
        total_tasks = num_tasks

        completed_tasks = 0
        overdue_tasks = 0

        for t in task_list:
            if t["completed"]:
                completed_tasks += 1
            elif t["due_date"] < datetime.today():
                overdue_tasks += 1

        incomplete_tasks = total_tasks - completed_tasks
        # Percentages calculation
        incomplete_percentage = (incomplete_tasks / total_tasks) * 100
        overdue_percentage = (overdue_tasks / total_tasks) * 100

        # Write task overview to task_overview.txt
        file.write("* * * * * * * * * * * * * * * * * * * * * * * * * * *")
        file.write("\t Task Overview\n")
        file.write("\t Total tasks: {}\n".format(total_tasks))
        file.write("\t Tasks Completed: {}\n".format(completed_tasks))
        file.write("\t Tasks Incompleted: {}\n".format(incomplete_tasks))
        file.write("\t Tasks Overdue: {}\n".format(overdue_tasks))
        file.write("\t % Tasks Incompleted: {:.0f}%\n".format(incomplete_percentage))
        file.write("\t % Tasks Overdue: {:.0f}%\n".format(overdue_percentage))
        file.write("* * * * * * * * * * * * * * * * * * * * * * * * * * *")

        # This set is created to ensure we can access username data without duplicates
        user_set = set(t["username"] for t in task_list)

        total_tasks_dict = defaultdict(int)
        completed_tasks_dict = defaultdict(int)
        overdue_tasks_dict = defaultdict(int)

        # Creating the user overview file
    with open("user_overview.txt", "w") as file:
        # Using the dictionaries created above, we will iterate through the task list to get the needed data for each task type
        for t in task_list:
            total_tasks_dict[t["username"]] += 1
            if t["completed"]:
                completed_tasks_dict[t["username"]] += 1
            elif t["due_date"] < datetime.today():
                overdue_tasks_dict[t["username"]] += 1

            # Using the above iteration, we will now write the user information to the file
        file.write("* * * * * * * * * * * * * * * * * * * * * * * * * * *")
        file.write("\t User Overview\n")
        file.write("\t Total No. of Users: {}\n ".format(len(user_set)))
        file.write("\t Total tasks: {}\n".format(total_tasks))
        file.write("\n")

        for user in user_set:
            file.write(user + "\n")
            file.write("\t {}'s Total Tasks: {}\n".format(user, total_tasks_dict[user]))
            file.write(
                "\t % of Total Tasks Assigned to User: {:.0f}%\n".format(
                    total_tasks_dict[user] / len(task_list) * 100, 2
                )
            )
            file.write(
                "\t % of User's Tasks Completed: {:.0f}%\n".format(
                    completed_tasks_dict[user] / total_tasks_dict[user] * 100, 2
                )
            )
            file.write(
                "\t % of User's Tasks Incompleted: {:.0f}%\n".format(
                    (total_tasks_dict[user] - completed_tasks_dict[user])
                    / total_tasks_dict[user]
                    * 100,
                    2,
                )
            )
            file.write(
                "\t % of User's Tasks Overdue: {:.0f}%\n".format(
                    overdue_tasks_dict[user] / total_tasks_dict[user] * 100, 2
                )
            )
            file.write("\n")
            file.write("* * * * * * * * * * * * * * * * * * * * * * * * * * *")

    print("Reports Generated Successfully")


def display_statistics():
    # Only admins can call this function
    if curr_user == "admin":
        # Calling generate reports will automatically update any changed information and make txt files if needed
        generate_reports()

        # This opens the task overview file to print 
        with open("task_overview.txt", "r") as task_file:
            task_overview = task_file.read()
            print("Task Overview:\n")
            print(task_overview)

            #The same is done for user overview
        with open("user_overview.txt", "r") as user_file:
            user_overview = user_file.read()
            print("User Overview\n")
            print(user_overview)
    
    # If the current user is not admin, this will be dispalyed 
    else:
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * *")
        print("\tThis function is reserved for admin only")
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * *")
    return


# Menu
while True:
    # Presenting the menu to the user and
    # Making sure that the user input is converted to lower case.
    print()
    menu = input(
        """Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports 
ds - Display statistics
e - Exit
: """
    ).lower()

    if menu == "r":
        reg_user()
    elif menu == "a":
        add_task()
    elif menu == "va":
        view_all()
    elif menu == "vm":
        view_mine()

    elif menu == "gr":
        generate_reports()

    elif menu == "ds":
        """If the user is an admin they can display statistics about number of users
        and tasks."""
        display_statistics()

    elif menu == "e":
        print("Goodbye!!!")
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
