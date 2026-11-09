"""Give every wiki page under FF8/ a permalink built from its folders' index.md titles and its own title.

A page that already has a permalink keeps it (unless --overwrite). Only the front matter is read and
only files that change are written, with their line endings kept.
Example: FF8/TechnicalReference/Field/Foo.md with "title: Foo Bar" -> /technical-reference/field/foo-bar/
"""
import argparse
import os
import re

DOCS_DIRECTORY = 'FF8'


def slug(text):
    text = text.lower().replace(' ', '-').replace('_', '-')
    return re.sub(r'[^a-z0-9\-]', '', text)


def front_matter_bounds(lines):
    """(start, end) line indexes of the opening and closing '---', or None when the page has no front matter."""
    if not lines or lines[0].strip() != '---':
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == '---':
            return 0, index
    return None


def front_matter_value(lines, key):
    bounds = front_matter_bounds(lines)
    if bounds is None:
        return None
    for line in lines[bounds[0] + 1:bounds[1]]:
        if line.strip().startswith(key + ':'):
            return line.strip()[len(key) + 1:].strip().strip('"').strip("'")
    return None


def read_lines(path):
    with open(path, 'r', encoding='utf-8', newline='') as file:
        return file.readlines()


def folder_title(folder):
    index_path = os.path.join(folder, 'index.md')
    if os.path.exists(index_path):
        return front_matter_value(read_lines(index_path), 'title')
    return None


def generate_permalink(file_path, title):
    """Folder part from each folder's index.md title (or the folder name), then the page title.
    An index.md gets its folder's permalink."""
    relative = os.path.relpath(file_path, DOCS_DIRECTORY).replace(os.sep, '/')
    folders = relative.split('/')[:-1]
    parts = []
    current = DOCS_DIRECTORY
    for folder in folders:
        current = os.path.join(current, folder)
        parts.append(slug(folder_title(current) or folder))
    if os.path.basename(file_path).lower() != 'index.md':
        parts.append(slug(title))
    return '/' + '/'.join(parts) + '/'


def update_front_matter(file_path, overwrite, dry_run):
    lines = read_lines(file_path)
    bounds = front_matter_bounds(lines)
    title = front_matter_value(lines, 'title')
    if bounds is None or not title:
        print(f"Skipping {file_path}: no front matter title.")
        return False

    new_permalink = generate_permalink(file_path, title)
    newline = '\r\n' if lines[0].endswith('\r\n') else '\n'
    new_line = f'permalink: {new_permalink}{newline}'
    for index in range(bounds[0] + 1, bounds[1]):
        if lines[index].strip().startswith('permalink:'):
            if not overwrite or lines[index] == new_line:
                return False
            lines[index] = new_line
            break
    else:
        lines.insert(bounds[1], new_line)

    print(f"{file_path}: permalink {new_permalink}")
    if not dry_run:
        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            file.writelines(lines)
    return True


def process_directory(directory, overwrite, dry_run):
    changed = 0
    for root, _, files in os.walk(directory):
        for file in sorted(files):
            if file.endswith('.md'):
                changed += update_front_matter(os.path.join(root, file), overwrite, dry_run)
    print(f"{changed} page(s) {'would change' if dry_run else 'changed'}.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate permalinks for the wiki Markdown pages.')
    parser.add_argument('--overwrite', action='store_true', help='Replace existing permalinks too')
    parser.add_argument('--dry-run', action='store_true', help='Only print what would change')
    args = parser.parse_args()
    process_directory(DOCS_DIRECTORY, args.overwrite, args.dry_run)
