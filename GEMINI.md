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

---

### `git_index.md` Generation Rules (Advanced)

To create a more structured and user-friendly `git_index.md` file, follow these rules:

1.  **Group by Folder:**
    Group the files by their parent directory. Each directory should have its own section with a heading.

2.  **Use Tables:**
    For each directory, create a Markdown table with the following columns:
    *   `File Name`: The name of the HTML file.
    *   `Last Updated`: The date when the file was last modified, in `YYYY-MM-DD` format.
    *   `Link`: A link to the file on the GitHub Pages website.

3.  **Sort by Date:**
    Within each table, sort the files by the "Last Updated" date in descending order (newest first).