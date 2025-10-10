from neuralintents import BasicAssistant
import sys

todos = []

def todo_show():
    print("Bot: Here are your Tasks:")
    for todo in todos:
            print(f"- {todo}")
def todo_remove():
    idx = int(input("Bot: enter the task you want to remove (number): "))-1
    if idx < len(todos):
        todos.pop(idx)
    else:
        print("Bot: Invalid task!")
def todo_add():
    item = input("Bot: what do you want to add?: ")
    todos.append(item)
    print(f'Bot: "{item}" successfully added to todos')
def bye():
    print("Good Bye!")
    sys.exit(0)
mappings = {"show_todos": todo_show,
            "delete_todo": todo_remove,
            "add_todo": todo_add,
            "goodbye":bye}
model = BasicAssistant("intents_file.json",mappings)
model.load_model()
while True:
    message = str(input("You: "))
    print(f"{model.process_input(message)}")