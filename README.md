# Project Structure Generator

A Python script to generate a project directory structure in a tree-like format, excluding files and directories ignored by a `.gitignore` file. The output is saved to a specified text file.

## Features
- Recursively generates a directory structure for a given root directory.
- Honors `.gitignore` patterns to exclude specified files and directories.
- Outputs the directory structure in a visually appealing tree format.

## Requirements
- Python 3.6 or higher
- The `pathspec` library for `.gitignore` pattern matching.

Install `pathspec` using pip:

```bash
pip install pathspec
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/darshxm/project-structure-generator.git
   cd project-structure-generator
   ```
2. Ensure you have the necessary dependencies installed.

## Usage
Run the script using Python:

```bash
python project_structure_generator.py [options]
```

### Options
| Option            | Description                                                                                       | Default                     |
|--------------------|---------------------------------------------------------------------------------------------------|-----------------------------|
| `-r`, `--root`    | Root directory of the project to generate the structure from.                                     | Current working directory   |
| `-o`, `--output`  | Path to the output text file where the structure will be saved.                                   | `project_structure.txt`     |
| `-g`, `--gitignore` | Path to the `.gitignore` file to use for filtering ignored files and directories.                | `.gitignore`                |

### Examples

#### Generate structure for the current directory:
```bash
python project_structure_generator.py
```

#### Specify a custom root directory:
```bash
python project_structure_generator.py -r /path/to/your/project
```

#### Specify a custom output file:
```bash
python project_structure_generator.py -o /path/to/output.txt
```

#### Use a custom `.gitignore` file:
```bash
python project_structure_generator.py -g /path/to/custom.gitignore
```

## Example Output
For a directory structure like this:
```
my_project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
└── README.md
```

The generated `project_structure.txt` will contain:
```
my_project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
└── README.md
```

## License
This project is licensed under the GNU GPL License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

---
