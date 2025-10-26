import os
import datetime
import glob

base_path = "/Users/joelho/Library/Mobile Documents/com~apple~CloudDocs/vscode_project/OCgithub/"
base_url = "https://joelhoty.github.io/ocgit/"

files = glob.glob(base_path + "**/*.html", recursive=True)

file_data = {}
for f in files:
    try:
        mtime = os.path.getmtime(f)
        dt = datetime.datetime.fromtimestamp(mtime)
        relative_path = f.replace(base_path, "")
        directory = os.path.dirname(relative_path)
        if directory == "":
            directory = "Root"
        if directory not in file_data:
            file_data[directory] = []
        
        file_data[directory].append({
            "file_name": os.path.basename(relative_path),
            "date": dt,
            "url": base_url + relative_path
        })
    except FileNotFoundError:
        pass

markdown = "# Project File Index\n\nThis file contains a list of all HTML files in the project, organized by folder.\n\n"

for directory in sorted(file_data.keys()):
    markdown += f"**{directory}**\n\n"
    markdown += "| File Name | Last Updated | Link |\n"
    markdown += "| --- | --- | --- |\n"
    
    sorted_files = sorted(file_data[directory], key=lambda x: x['date'], reverse=True)
    
    for data in sorted_files:
        markdown += f"| {data['file_name']} | {data['date'].strftime('%Y-%m-%d')} | [Link]({data['url']}) |\n"
    
    markdown += "\n"

with open("git_index.md", "w") as f:
    f.write(markdown)