import os
from datetime import datetime

DATETIME_STRING_FORMAT = "%d-%m-%Y"


def reg_user():
    '''Register a new user.'''
    username_password = load_user_data()

    while True:
        username = input("Enter a new username: ")
        if username in username_password:
            print("\nUsername already exists. Please try again.\n")
        else:
            password = input("Enter a password: ")
            username_password[username] = password
            save_user_data(username_password)
            print("\nUser registered successfully.")
            break


def add_task():
    '''Add a new task.'''
    task_list = load_task_data()
    username = input("Enter the username of the person the task is assigned to: ")
    title = input("Enter the title of the task: ")
    description = input("Enter the description of the task: ")
    # Ensure user enters the date in correct format
    while True:
        due_date = input("Enter the due date of the task (in format DD MMM YYYY): ")
        # Ensure date format is correct
        due_date = due_date.replace(" ","-")
        try:
            datetime.strptime(due_date, DATETIME_STRING_FORMAT)
            assigned_date = datetime.now().date()
            break
        except ValueError:
            print("\nPlease enter the date in the correct format\n")
        

    task = {
        "username": username,
        "title": title,
        "description": description,
        "due_date": datetime.strptime(due_date, DATETIME_STRING_FORMAT).date(),
        "assigned_date": assigned_date,
        "completed": False
    }

    task_list.append(task)
    save_task_data(task_list)
    print("Task added successfully.")


def view_all():
    '''View all tasks.'''
    task_list = load_task_data()

    print("===== All Tasks =====")
    for i, task in enumerate(task_list, start=1):
        print(f"Task {i}:")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Assigned to: {task['username']}")
        print(f"Due date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Assigned date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Completed: {'Yes' if task['completed'] else 'No'}")
        print("-----------------------")
    print(f"Total tasks: {len(task_list)}")


def view_mine():
    '''View tasks assigned to the current user.'''
    task_list = load_task_data()
    current_user = get_current_user()
    edit_tasks = []

    print(f"\n===== Tasks assigned to {current_user} =====")
    for i, task in enumerate(task_list, start=1):
        if task['username'] == current_user:
            print(f"Task {i}:")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Due date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Assigned date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Completed: {'Yes' if task['completed'] else 'No'}")
            print("-----------------------")
            if task['completed'] == False:
                edit_tasks.append(i)
            

    while True:
        try:
            user_choice = int(input('''\nWould you like to:
\tEdit a specific task (Enter 1)
\tReturn to the main menu (Enter -1)

Enter an option: '''))
            
            if user_choice == 1 or -1:
                if user_choice == -1:
                    break
                elif user_choice == 1:
                    print()
                    # Print task number and titles for current user
                    for i in edit_tasks:
                        print(f"{i}: {task_list[i-1]['title']}")
                    
                    # User chooses the task to edit
                    while True:
                        try:
                            task_choice = int(input('''\nEnter the task number of the task you wish to edit: '''))
                            if task_choice in edit_tasks:
                                while True:
                                    try:
                                        edit_choice = int(input('''\nWould you like to:
    \t1. Mark the task as complete? (Enter 1)
    \t2. Edit the task? (Enter 2)'''))
                                        if edit_choice == 1 or 2:
                                            if edit_choice == 1:
                                                # the completed variable of the choosen task is set to complete
                                                task_list[task_choice-1]['completed'] = True
                                                save_task_data(task_list)
                                                print(f"Task {task_choice} has been set to completed.\n")
                                                break
                                            elif edit_choice == 2:
                                                # use chooses whether to change user that the task is assigned to or its due date
                                                while True:
                                                    try:
                                                        edit2 = int(input('''\nWould you like to change the due date or the person assigned to the task?
    \tDue date [Enter 1]
    \tAssigned user [Enter 2]'''))
                                                        if edit2 == 1 or 2:
                                                            if edit2 == 1:
                                                                while True:
                                                                    due_date = input("Enter the new due date of the task (in format DD MMM YYYY): ")
                                                                    # Ensure date format is correct
                                                                    due_date = due_date.replace(" ","-")
                                                                    try:
                                                                        task_list[task_choice-1]['due_date'] = datetime.strptime(due_date, DATETIME_STRING_FORMAT).date()
                                                                        save_task_data(task_list)
                                                                        print(f"\nThe due date for task {task_choice} has been changed to {due_date}.\n")
                                                                        break
                                                                    except ValueError:
                                                                        print("\nPlease enter the date in the correct format\n")
                                                            elif edit2 == 2:
                                                                new_user = input(f"\nPlease enter the new user to be assigned to task {task_choice}.\nNew User: ")
                                                                task_list[task_choice-1]['username'] = new_user
                                                                save_task_data(task_list)
                                                                print(f"\nThe new user for task {task_choice} has been changed to {new_user}.\n")
                                                            break
                                                        else:
                                                            print("\nPlease enter a valid option.")
                                                    except ValueError:
                                                        print("\nPlease enter a valid option.")
                                                break
                                        else:
                                            print("\nPlease choose a task assigned to you.")
                                    except ValueError:
                                        print("\nPlease enter a valid option.")
                                break
                            else:
                                print("\nPlease enter a task that is assigned to you.")
                        except ValueError:
                                print("\nPlease enter a valid option.")
                    break
            else:
                print("\nPlease enter a valid option.\n")

        except ValueError:
            print("\nPlease enter a valid option.")


def generate_reports():
    '''Generate task and user overview reports.'''
    task_list = load_task_data()
    username_password = load_user_data()

    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(task['due_date'] < datetime.now().date() and not task['completed'] for task in task_list)

    tasks_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks > 0 else 0

    user_count = len(username_password)

    print("Generating task overview report...")
    with open("task_overview.txt", "w") as f:
        f.write("===== Task Overview =====\n")
        f.write(f"Total tasks: {total_tasks}\n")
        f.write(f"Completed tasks: {completed_tasks}\n")
        f.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        f.write(f"Overdue tasks: {overdue_tasks}\n")
        f.write(f"Tasks percentage: {tasks_percentage:.2f}%\n")
        f.write(f"Overdue percentage: {overdue_percentage:.2f}%\n")
    print("Task overview report generated successfully.")

    print("Generating user overview report...")
    with open("user_overview.txt", "w") as f:
        f.write("===== User Overview =====\n")
        f.write(f"Total users: {user_count}\n")
        f.write(f"Total tasks: {total_tasks}\n")

        for username, password in username_password.items():
            user_tasks = sum(task['username'] == username for task in task_list)
            user_completed = sum(task['username'] == username and task['completed'] for task in task_list)
            user_uncompleted = user_tasks - user_completed
            user_overdue = sum(task['username'] == username and task['due_date'] < datetime.now().date() and not task['completed'] for task in task_list)

            user_tasks_percentage = (user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            user_completed_percentage = (user_completed / user_tasks) * 100 if user_tasks > 0 else 0
            user_uncompleted_percentage = (user_uncompleted / user_tasks) * 100 if user_tasks > 0 else 0
            user_overdue_percentage = (user_overdue / user_uncompleted) * 100 if user_uncompleted > 0 else 0

            f.write("-----------------------\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
            f.write(f"Tasks assigned: {user_tasks}\n")
            f.write(f"Tasks assigned percentage: {user_tasks_percentage:.2f}%\n")
            f.write(f"Tasks completed percentage: {user_completed_percentage:.2f}%\n")
            f.write(f"Tasks uncompleted percentage: {user_uncompleted_percentage:.2f}%\n")
            f.write(f"Tasks overdue percentage: {user_overdue_percentage:.2f}%\n")

        f.write("-----------------------\n")
    print("User overview report generated successfully.")


def load_user_data():
    '''Load user data from file.'''
    if not os.path.exists("user.txt"):
        return {}

    with open("user.txt", "r") as f:
        lines = f.readlines()

    username_password = {}
    for line in lines:
        # Check if any blank spaces left in file by mistake
        if line.isspace() == True:
            break
        else:
            username, password = line.strip().split(", ")
            username_password[username] = password

    return username_password


def save_user_data(username_password):
    '''Save user data to file.'''
    with open("user.txt", "w") as f:
        for username, password in username_password.items():
            f.write(f"{username}, {password}\n")


def load_task_data():
    '''Load task data from file.'''
    if not os.path.exists("tasks.txt"):
        return []

    with open("tasks.txt", "r") as f:
        lines = f.readlines()

    task_list = []
    for line in lines:
        username, title, description, due_date, assigned_date, completed = line.strip().split(", ")
        task = {
            "username": username,
            "title": title,
            "description": description,
            "due_date": datetime.strptime(due_date, DATETIME_STRING_FORMAT).date(),
            "assigned_date": datetime.strptime(assigned_date, DATETIME_STRING_FORMAT).date(),
            "completed": completed == "Yes"
        }
        task_list.append(task)

    return task_list


def save_task_data(task_list):
    '''Save task data to file.'''
    with open("tasks.txt", "w") as f:
        for task in task_list:
            username = task['username']
            title = task['title']
            description = task['description']
            due_date = task['due_date'].strftime(DATETIME_STRING_FORMAT)
            assigned_date = task['assigned_date'].strftime(DATETIME_STRING_FORMAT)
            completed = "Yes" if task['completed'] else "No"
            f.write(f"{username}, {title}, {description}, {due_date}, {assigned_date}, {completed}\n")


def get_current_user():
    '''Get the username of the current user.'''
    return input("\nEnter your username: ")

def display_stats():
    ''' Generate up to date report on users and then print to screen'''
    generate_reports()

    print()
    with open("user_overview.txt", "r") as f:
        Lines = f.readlines()

        count = 0
        # Strips the newline character
        for line in Lines:
            count += 1
            print(line.strip())

def main():
    '''Main function.'''
    while True:
        print("\n===== Task Manager Menu =====")
        print("1. Register User (Enter 'r')")
        print("2. Add Task (Enter 'a')")
        print("3. View All Tasks (Enter 'va')")
        print("4. View My Tasks (Enter 'vm')")
        print("5. Generate Reports (Enter 'gr')")
        print("6. Display Statstics (Enter 'ds')")
        print("7. Exit (Enter 'x')\n")
        
        # Ask user to choose an option
        option = input("Enter an option: ")
        if option == "r":
            reg_user()
        elif option == "a":
            add_task()
        elif option == "va":
            view_all()
        elif option == "vm":
            view_mine()
        elif option == "gr":
            generate_reports()
        elif option == "ds":
            display_stats()
        elif option == "x":
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
