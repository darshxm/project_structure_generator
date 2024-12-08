import os
import argparse
import pathspec

# Define tree characters
TREE_BRANCH = '├── '
TREE_LAST_BRANCH = '└── '
TREE_VERTICAL = '│   '
TREE_SPACE = '    '

def load_gitignore_patterns(gitignore_path):
    """
    Load patterns from a .gitignore file using pathspec.
    """
    if not os.path.exists(gitignore_path):
        return pathspec.PathSpec.from_lines('gitwildmatch', [])
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return pathspec.PathSpec.from_lines('gitwildmatch', lines)

def is_ignored(path, spec):
    """
    Check if a given path is ignored based on the spec.
    The path should be relative to the project root.
    """
    return spec.match_file(path)

def generate_structure(root_dir, output_file, ignore_spec):
    # We'll write to the file once at the end
    lines = []

    # Print the top directory name
    root_name = os.path.basename(root_dir)
    if not root_name:
        # If the directory is something like '/'
        root_name = root_dir.strip(os.sep).split(os.sep)[-1] or '.'
    lines.append(root_name + "/")

    # We'll use os.walk to traverse the directory
    # For the tree drawing, we need a stack to know what prefixes to print
    # per directory level. Instead of a stack of prefixes, we'll generate
    # the tree per directory separately.
    
    # We'll store directory listings in memory first, then format.
    dir_structure = {}
    
    for current_root, dirs, files in os.walk(root_dir, topdown=True):
        # Compute relative path from root_dir
        rel_dir = os.path.relpath(current_root, root_dir)
        if rel_dir == '.':
            rel_dir = ''  # top-level directory

        # Filter directories
        filtered_dirs = []
        for d in dirs:
            d_path = os.path.join(rel_dir, d) if rel_dir else d
            # Add a trailing slash to directories before checking ignore
            if not is_ignored(d_path + '/', ignore_spec):
                filtered_dirs.append(d)
        dirs[:] = filtered_dirs

        # Filter files
        filtered_files = []
        for f_name in files:
            f_path = os.path.join(rel_dir, f_name) if rel_dir else f_name
            if not is_ignored(f_path, ignore_spec):
                filtered_files.append(f_name)

        dirs.sort()
        filtered_files.sort()

        # Store them
        dir_structure[rel_dir] = (dirs, filtered_files)

    # Now we have a dictionary of directories -> (subdirs, files)
    # We need to print them in a tree format starting from '' (the root).

    def print_tree(prefix, rel_dir):
        dirs, files = dir_structure[rel_dir]
        items = dirs + files
        count = len(items)

        for i, item in enumerate(items):
            connector = TREE_LAST_BRANCH if i == count - 1 else TREE_BRANCH
            line = prefix + connector + item
            lines.append(line)

            # If it's a directory, recurse
            if item in dirs:
                # For subdirectories, build their relative path
                sub_rel_dir = os.path.join(rel_dir, item) if rel_dir else item
                # Add a trailing slash to printed directories for clarity
                lines[-1] += '/'
                # Depending on whether this is the last item, choose prefix
                if i == count - 1:
                    # Last item at this level
                    new_prefix = prefix + TREE_SPACE
                else:
                    # Not last item
                    new_prefix = prefix + TREE_VERTICAL
                
                # Recurse into the subdirectory
                print_tree(new_prefix, sub_rel_dir)

    # Print the tree starting from the root directory
    print_tree('', '')

    # Write all lines to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + "\n")

def main():
    parser = argparse.ArgumentParser(description="Generate project structure and save to a text file.")
    parser.add_argument(
        '-r', '--root',
        type=str,
        default=os.getcwd(),
        help='Root directory of the project (default: current directory)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='project_structure.txt',
        help='Output file path (default: project_structure.txt)'
    )
    parser.add_argument(
        '-g', '--gitignore',
        type=str,
        default='.gitignore',
        help='Path to the .gitignore file (default: .gitignore)'
    )
    
    args = parser.parse_args()
    
    root_dir = os.path.abspath(args.root)
    gitignore_path = os.path.join(root_dir, args.gitignore)
    output_file = os.path.abspath(args.output)
    
    # Load ignore patterns
    ignore_spec = load_gitignore_patterns(gitignore_path)
    
    print(f"Generating project structure for: {root_dir}")
    generate_structure(root_dir, output_file, ignore_spec)
    print(f"Project structure has been saved to: {output_file}")

if __name__ == "__main__":
    main()
