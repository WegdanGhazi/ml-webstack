import os

def get_file_path(fileName):

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, fileName)
    return abs_file_path