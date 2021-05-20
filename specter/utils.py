import os

def get_all_files(path, ignore=[]):
    output = []
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            if not any([i in path for i in ignore]):
                output.append(path)
    return output


