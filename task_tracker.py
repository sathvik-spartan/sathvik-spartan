import json
import argparse
from pathlib import Path

# File path for storing tasks
TASK_FILE = Path("tasks.json")

# Load tasks from a JSON file if it exists, else create an empty list
def load_tasks():
    if TASK_FILE.exists():
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to a JSON file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Add a task to the task list
def add_task(task_desc):
    tasks = load_tasks()
    tasks.append({"task": task_desc, "done": False})
    save_tasks(tasks)
    print(f"Added task: {task_desc}")

# List all tasks, showing their status
def list_tasks():
    tasks = load_tasks()
    if tasks:
        print("\nYour Tasks:")
        for idx, task in enumerate(tasks, 1):
            status = "✓" if task["done"] else "✗"
            print(f"{idx}. [{status}] {task['task']}")
    else:
        print("No tasks to show.")

# Mark a task as complete
def mark_task(task_number):
    tasks = load_tasks()
    try:
        task = tasks[task_number - 1]
        task["done"] = True
        save_tasks(tasks)
        print(f"Marked task '{task['task']}' as complete.")
    except IndexError:
        print("Invalid task number.")

# Remove a task by its number
def remove_task(task_number):
    tasks = load_tasks()
    try:
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        print(f"Removed task: {removed_task['task']}")
    except IndexError:
        print("Invalid task number.")

# Set up CLI arguments and functions
parser = argparse.ArgumentParser(description="Task Tracking CLI App")
subparsers = parser.add_subparsers(dest="command")

# Add task command
add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("--task", type=str, required=True, help="Task description")

# List tasks command
subparsers.add_parser("list", help="List all tasks")

# Mark task command
mark_parser = subparsers.add_parser("mark", help="Mark a task as complete")
mark_parser.add_argument("--task-number", type=int, required=True, help="Task number to mark as complete")

# Remove task command
remove_parser = subparsers.add_parser("remove", help="Remove a task")
remove_parser.add_argument("--task-number", type=int, required=True, help="Task number to remove")

# Parse arguments and call corresponding function
args = parser.parse_args()
if args.command == "add":
    add_task(args.task)
elif args.command == "list":
    list_tasks()
elif args.command == "mark":
    mark_task(args.task_number)
elif args.command == "remove":
    remove_task(args.task_number)
else:
    parser.print_help()
