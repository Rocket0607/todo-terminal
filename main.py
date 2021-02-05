import todoist
import argparse
import sys

api = todoist.TodoistAPI("9e76745d59cbda40acc52841cf097d3950c1bbe7")
api.sync()

def todo(args):
    project_name = args.p
    add_item = args.a
    remove_item = args.r
    complete_item = args.c
    project_id = None
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

    for item in api.items.all():
        if item["checked"] == 0 and item["project_id"] == project_id:
            print(item["content"])

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--p", type = str, default="Inbox", help = "What is the name of the project. Use --p + the name of the project you want to see. Defaults to your inbox.")

    parser.add_argument("--a", type = str, default = None, help = "This is for if u would like to add an item. Use --a + the name of the item you would like to add. Use --p to choose which project.")

    parser.add_argument("--r", type = str, default = None, help = "This is for if u would like to remove an item. Use --r + the name of the item you want to remove. Use --p to choose which project.")

    parser.add_argument("--c", type = str, default = None, help = "This is for if u would like to complete an item. Use --c + the name of the item you want to complete. Use --p to choose which project.")

    args = parser.parse_args()
    sys.stdout.write(str(todo(args)))

if __name__ == "__main__":
    main()
