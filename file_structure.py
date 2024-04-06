import os

path = 'calculator-app'

# - represents the subfiles
def print_directory_structure(path, indent=0):
    print('-' * indent + os.path.basename(path))
    if os.path.isdir(path):
        for child in os.listdir(path):
            child_path = os.path.join(path, child)
            print_directory_structure(child_path, indent + 1)

print_directory_structure(path)

# print relative paths
def print_relative_paths(path):
    parent_path = os.path.dirname(path)
    for root, dirs, files in os.walk(parent_path):
        for file in files:
            print(os.path.relpath(os.path.join(root, file), parent_path))

# Test the function
print_relative_paths(path)