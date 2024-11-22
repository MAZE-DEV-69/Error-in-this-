import json
from argon2 import PasswordHasher

ph = PasswordHasher()


# Load User
def load_user_id():
    try:
        with open("user.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_user_id(user):
    with open("user.json", "w") as file:
        json.dump(user, file, indent=4)


def hash_pass(password):
    return ph.hash(password)


def verify_user(user, username, password):
    if username in user:
        try:
            ph.verify(user[username], password)
            return True
        except:
            return False
    return False


def register_id(user, username, password):
    if username in user:
        print("Please choose another username; this one is already taken.")
    else:
        hashed_pass = hash_pass(password)
        user[username] = hashed_pass
        print("Congratulations! You have been registered.")


# Load Task
def load_task():
    try:
        with open("task.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_task(all_task):
    with open("task.json", "w") as file:
        json.dump(all_task, file, indent=4)


def get_LIUT(all_task, username):
    return all_task.get(username, [])


def set_LIUT(all_task, username, user_task):
    all_task[username] = user_task
    save_task(all_task)


# Display Task
def display_task(task):
    if not task:
        print("No tasks found. You are either very efficient or have no tasks.")
    else:
        for idx, t in enumerate(task, start=1):
            print(f"{idx}. {t['task']} - {'COMPLETED' if t['COMPLETED'] else 'Pending'}")


# Add Task
def add_task(all_task, task_name, username):
    user_task = get_LIUT(all_task, username)
    user_task.append({"task": task_name, "COMPLETED": False})
    set_LIUT(all_task, username, user_task)
    print(f"Task '{task_name}' added successfully.")


def mark_task_complete(all_task, username, task_index):
    user_task = get_LIUT(all_task, username)
    if 0 <= task_index < len(user_task):
        user_task[task_index]["COMPLETED"] = True
        set_LIUT(all_task, username, user_task)
        print(f"Task '{user_task[task_index]['task']}' marked as completed.")
    else:
        print("Invalid task index.")


def delete_task(all_task, username, task_index):
    user_task = get_LIUT(all_task, username)
    if 0 <= task_index < len(user_task):
        removed_task = user_task.pop(task_index)
        set_LIUT(all_task, username, user_task)
        print(f"Task '{removed_task['task']}' deleted successfully.")
    else:
        print("Invalid task index.")


def migrate_old_files(default_user="default_user"):
    try:
        with open("task.json", "r") as file:
            old_task = json.load(file)

        new_file = {default_user: old_task}
        with open("task.json", "w") as file:
            json.dump(new_file, file, indent=4)
        print("Old tasks migrated successfully.")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No old tasks found. Starting fresh!")
        with open("task.json", "w") as file:
            json.dump({}, file, indent=4)


# Main Function
def main():
    user = load_user_id()
    all_task = load_task()
    logged_in_user = None

    while True:
        if logged_in_user is None:
            print("\nWelcome to Task Management System v2.0")
            print("1. Login")
            print("2. Register")
            print("3. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                if verify_user(user, username, password):
                    logged_in_user = username
                    print(f"Welcome back, {logged_in_user}!")
                else:
                    print("Invalid username or password.")
            elif choice == "2":
                username = input("Enter a new username: ")
                password = input("Enter a secure password: ")
                register_id(user, username, password)
                save_user_id(user)
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
        else:
            print(f"\nLogged in as {logged_in_user}")
            print("1. Add Task")
            print("2. Mark Task as Completed")
            print("3. Display Tasks")
            print("4. Delete Task")
            print("5. Logout")

            choice = input("Choose an option: ")

            if choice == "1":
                task_name = input("Enter the name of the task: ")
                add_task(all_task, task_name, logged_in_user)
            elif choice == "2":
                display_task(get_LIUT(all_task, logged_in_user))
                try:
                    task_index = int(input("Enter task number to mark as completed: ")) - 1
                    mark_task_complete(all_task, logged_in_user, task_index)
                except ValueError:
                    print("Invalid input. Enter a valid task number.")
            elif choice == "3":
                display_task(get_LIUT(all_task, logged_in_user))
            elif choice == "4":
                display_task(get_LIUT(all_task, logged_in_user))
                try:
                    task_index = int(input("Enter task number to delete: ")) - 1
                    delete_task(all_task, logged_in_user, task_index)
                except ValueError:
                    print("Invalid input. Enter a valid task number.")
            elif choice == "5":
                logged_in_user = None
                print("Logged out successfully.")
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    migrate_old_files()
    main()