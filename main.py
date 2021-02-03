import todoist

api = todoist.TodoistAPI("9e76745d59cbda40acc52841cf097d3950c1bbe7")
project_name = input("project: ")
project_id = None

for project in api.state["projects"]:
    if project["name"] == project_name:
        project_id = project["id"]
    if project_name == "":
        project_id = 2233390427

for item in api.items.all():
    if item["project_id"] == project_id:
        print(item["content"])
