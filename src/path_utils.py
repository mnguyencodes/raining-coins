import os

def get_parent_dir(path, directories=1):
    path_result = None
    for i in range(directories):
        path_result = get_parent_dir(path.rpartition(os.sep)[0], i)
    return path_result or path

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    print(get_parent_dir(root_dir()))