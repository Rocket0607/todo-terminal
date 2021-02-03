import todoist
import argparse
import sys

api = todoist.TodoistAPI("9e76745d59cbda40acc52841cf097d3950c1bbe7")

def print_todos(args):
    project_name = args.p
    project_id = None
    for project in api.state["projects"]:
        if project["name"] == project_name:
            project_id = project["id"]
        if project_name == "":
            project_id = 2233390427

    for item in api.items.all():
        if item["project_id"] == project_id:
            print(item["content"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=str, default="Inbox", help="What is the name of the project")
    args = parser.parse_args()
    sys.stdout.write(str(print_todos(args)))

if __name__ == "__main__":
    main()
