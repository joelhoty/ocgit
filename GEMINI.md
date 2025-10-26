### Update `git_index.md`

To update the `git_index.md` file, follow these steps:

1.  **Find all HTML files:**
    Use the `glob` tool with the pattern `**/*.html` to find all HTML files in the repository.

2.  **Generate index content:**
    For each HTML file, create a markdown list item with a link to its corresponding GitHub Pages URL. The base URL is `https://joelhoty.github.io/ocgit/`.

3.  **Write to `git_index.md`:**
    Write the generated markdown content to the `git_index.md` file.

4.  **Commit the changes:**
    Add the `git_index.md` file to the staging area and commit the changes.
