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
        json.dump(user, file)

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
        print("PLS CHOOSE ANOTHER USERNAME AS ALREADY BEFORE YOU TOOK THIS NAME HAHA LOL BETTER LUCK NEXT TIME ")
    else:
        hashed_pass = hash_pass(password)
        user[username] = hashed_pass
        print("CONGRATS YOU HAVE BEEN REGISTERED NOW YOU ARE PART OF SKYNET... JUST JOKING YOU ARE INTO MY MATRIX HAHAHA")

# Load Task
def load_task():
    try:
        with open("task.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_task(task):
    with open("task.json", "w") as file:
        json.dump(task, file)

# Dis Task 
def display_task(task):
    if not task:
        print("SO YOU HAVE 69 TASK LEFT ! \n WAIT LET ME SEE AGAIN U HAVE NO TASK LEFT OR U DIDNT HAD ANY TASK \n I GUESS ITS LUCKY FOR YOU BECAUSE YOU HAVE NO TASK OR YOU ARE A LAZY GUY BUT HAVE FUN")
    else:
        for idx, task in enumerate(task, start=1):
            print(f" {idx}. {task['task']}) - {'COMPLETED' if task['COMPLETED'] else 'pending'} ")

# Add Task
def add_task(task, task_name):
    task.append({"task": task_name, "COMPLETED": False})
    print(f"task '{task_name}' added successfully so now go and complete the task ")

def mark_task_complete(task, task_index):
    if 0 <= task_index < len(task):
        task[task_index]["COMPLETED"] = True
        print(f"task '{task[task_index]['task']}' marked as completed")  
    else:
        print("INVALID TASK INDEX")

def delete_task(task, task_index):
    if 0 <= task_index < len(task):
        removed_task = task.pop(task_index) 
        print(f"Task '{removed_task['task']}' deleted successfully!")
    else:
        print("Invalid task index.")	

def migrate_old_files(default_user="default_user"):
    try:
        with open("task.json", "r") as file:
            old_task = json.load(file)

        new_file = {default_user: old_task}
        with open("task.json", "w") as file:
            json.dump(new_file, file, indent=4)
        print("OLD FILES HAVE BEEN MIGRATED INTO NEW FILES THANKS FOR CHOOSING MAZE TODO LIST SERVICE")
    except (FileNotFoundError, json.JSONDecodeError):
        print("WELL CONGRATS NO OLD FILE FOUND OR MAYBE ITS BAD FOR YOU IF YOU HAD OLD FILES BUT LETS START FRESH")
        with open("task.json", "w") as file:
            json.dump({}, file, indent=4)

def main():
    user = load_user_id()
    task = load_task()
    logged_in_user = None  

    while True:
        if logged_in_user is None:
            print(" \n WELCOM TO MY TASK MANAGMENT SYSTEM V.1")
            print("1.  Login")
            print("2.  Register")
            print("3.  Exit")
            
            choice = input("PLEASE CHOOSE A OPTION :- ")
            
            if choice == "1":
                username = input("PLEASE ENTER YOUR USERNAME :- ")
                password = input("PLEASE ENTER YOUR PASSWORD :- ")
                if verify_user(user, username, password):
                    logged_in_user = username
                    print(f"WELCOME BACK {logged_in_user}")
                else:
                    print("INVALID USERNAME OR PASSWORD")
                    
            elif choice == "2":
                username = input("PLEASE ENTER NEW USERNAME :- ")
                password = input("PLEASE ENTER A SECRET HARD PASSWORD :- ")
                register_id(user, username, password)
                save_user_id(user)
            elif choice == "3":
                print("GOODBYE ! ")
                break
            else:
                print("INVALID CHOICE. PLEASE TRY AGAIN.")
        else:
            print(f"\nLogged in as {logged_in_user}")
            print("1. Add Task")
            print("2. Mark Task As Completed")
            print("3. Display Tasks")
            print("4. Logout")
            choice = input("Please choose an option: ")

            if choice == "1":
                task_name = input("Enter the name of the task: ")
                add_task(task, task_name)
                save_task(task)
            elif choice == "3":
                display_task(task)
            elif choice == "4":
                logged_in_user = None
                print("LOGGED OUT SUCCESSFULLY.")
            elif choice == "2":
                display_task(task)
                try:
                    task_index = int(input("ENTER TASK NUMBER WHICH U WANNA MARK AS COMPLETED :- ")) - 1
                    mark_task_complete(task, task_index)
                    save_task(task)
                    display_task(task)
                except ValueError:
                    print("CMON MAN...JUST DO AS MY CODE SAYS DONT POKE YOUR INNER THAUGHT AND TRY TO FIND EASTER EGG WELL..YEAH THIS IS THE ONE BUT NOT ANYMORE")
            else:
                print("INVALID CHOICE. PLEASE TRY AGAIN.")

if __name__ == "__main__":
    migrate_old_files()
    main()