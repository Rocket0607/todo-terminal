import todoist
import argparse
from colorama import Fore
import datetime
from datetime import date
import sys
import os

def todo(args):
    project_name = args.p
    add_item = args.a
    remove_item = args.r
    complete_item = args.c
    new_project = args.ap
    list_projects = args.lp
    archived = args.archived
    remove_project = args.rp
    api_key = args.set_api_key
    program_path = os.environ["HOME"]
    project_id = None

    if api_key != None:
        with open(program_path + "/Documents/todo-terminal/key.txt", "w") as f:
            f.write(api_key)

    with open(program_path + "/Documents/todo-terminal/key.txt", "r") as f:
        key = f.read()

    api = todoist.TodoistAPI(key)
    api.sync()

    for project in api.state["projects"]:
        if project["name"] == project_name:
            project_id = project["id"]

    if add_item != None:
        item = api.items.add(add_item, project_id = project_id)
        api.commit()

    if remove_item != None:
        for item in api.items.all():
            if item["checked"] == 0 and item["content"] == remove_item and item["project_id"] == project_id:
                item = api.items.get_by_id(item["id"]) 
                item.delete()
                api.commit()

    if complete_item != None:
        for item in api.items.all():
            if item["content"] == complete_item and item["project_id"] == project_id:
                item = api.items.get_by_id(item["id"]) 
                item.complete()
                api.commit()

    if remove_project != None:
        for project in api.projects.all():
            if project["name"] == remove_project:
                deleted_project = api.projects.get_by_id(project["id"])
                deleted_project.delete()
                api.commit()
                list_projects = True

    if new_project != None:
        project = api.projects.add(new_project)
        api.commit()
        list_projects = True
    
    if list_projects and not archived:
        for project in api.projects.all():
            if project["is_archived"] == 0:
                print(project["name"])

    elif list_projects and archived:
        for project in api.projects.all():
            print(project["name"])

    else:
        for item in api.items.all():
            if item != None:
                if item["checked"] == 0 and item["project_id"] == project_id:
                    if item["due"] != None:
                        due_date = datetime.datetime.strptime(item["due"]["date"], "%Y-%m-%d")
                        if date.today() > due_date.date():
                            print(item["content"] + " | " + Fore.RED + item["due"]["string"])
                        else:
                            print(item["content"] + " | " + item["due"]["string"])
                    else:
                        print(item["content"] +" | "+ "No due date")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--p", type = str, default="Inbox", help = "What is the name of the project. Use --p + the name of the project you want to see. Defaults to your inbox.")

    parser.add_argument("--a", type = str, default = None, help = "This is for if u would like to add an item. Use --a + the name of the item you would like to add. Use --p to choose which project.")

    parser.add_argument("--r", type = str, default = None, help = "This is for if u would like to remove an item. Use --r + the name of the item you want to remove. Use --p to choose which project.")

    parser.add_argument("--ap", type = str, default = None, help = "This is to add a new project. Use --ap + name of new project.")

    parser.add_argument("--lp", action = "store_true", help = "This is to list all projects")

    parser.add_argument("--archived", action = "store_true", help = "This is to list all projects")

    parser.add_argument("--rp", type = str, default = None, help = "This is to remove a project. Use --rp + name of project.")

    parser.add_argument("--c", type = str, default = None, help = "This is for if u would like to complete an item. Use --c + the name of the item you want to complete. Use --p to choose which project.")

    parser.add_argument("--set-api-key", type = str, default = None, help = "use this to set your api key. Go to the todoist website. Go to settings and click on the integrations tab and the key will be at the botton of that page.")

    parser.add_argument("--set-program-path", type = str, default = None, help = "enter --set-program-path + path to where this program was installed. This is to help set your api key")

    args = parser.parse_args()
    sys.stdout.write(str(todo(args)))

if __name__ == "__main__":
    main()
