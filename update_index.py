import os
import subprocess
from datetime import datetime

def get_git_last_updated(file_path):
    try:
        # Execute the git log command to get the last commit date
        commit_date = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cd', '--date=short', '--', file_path],
            stderr=subprocess.PIPE,
            text=True
        ).strip()
        if commit_date:
            return commit_date
    except subprocess.CalledProcessError:
        # This could happen if the file is not tracked by Git
        pass
    
    # Fallback to file modification time if Git fails
    return datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')

def main():
    base_url = "https://joelhoty.github.io/ocgit/"
    root_dir = "/Users/joelho/Library/Mobile Documents/com~apple~CloudDocs/vscode_project/OCgithub"
    
    html_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    grouped_files = {}
    for file_path in html_files:
        # Use os.path.relpath to get the path relative to the root_dir
        relative_path = os.path.relpath(file_path, root_dir)
        directory = os.path.dirname(relative_path)
        
        if directory not in grouped_files:
            grouped_files[directory] = []
        
        grouped_files[directory].append({
            "path": file_path,
            "name": os.path.basename(file_path),
            "rel_path": relative_path
        })

    # Sort directories by name
    sorted_directories = sorted(grouped_files.keys())

    # Start markdown content
    markdown_content = "# Git Index\n\n"

    for directory in sorted_directories:
        if directory:
            markdown_content += f"## {directory}\n\n"
        else:
            markdown_content += "## Root\n\n"

        # Prepare data for sorting
        file_data = []
        for file_info in grouped_files[directory]:
            last_updated = get_git_last_updated(file_info["path"])
            file_data.append({
                "name": file_info["name"],
                "last_updated": last_updated,
                "link": f"{base_url}{file_info['rel_path']}"
            })

        # Sort files by last updated date (descending)
        sorted_files = sorted(file_data, key=lambda x: x['last_updated'], reverse=True)

        # Create markdown table
        markdown_content += "| File Name | Last Updated | Link |\n"
        markdown_content += "|---|---|---|\n"
        for file_info in sorted_files:
            markdown_content += f"| {file_info['name']} | {file_info['last_updated']} | [{file_info['name']}]({file_info['link']}) |\n"
        markdown_content += "\n"

    # Write to git_index.md
    with open(os.path.join(root_dir, "git_index.md"), "w") as f:
        f.write(markdown_content)

if __name__ == "__main__":
    main()
