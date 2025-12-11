import argparse
from pathlib import Path
def recursive_replace(path, find_text, replace_text):
    # grab all python files in this folder, replace
    for file_path in path.rglob("*.py"):
        replace_in_file(file_path, find_text, replace_text)
    # go through all sub folders
    for x in path.iterdir():
        if x.is_dir():
            # grab dictionaries, reiterate recursively
            # honestly could probably combine this and previous loop, but this is faster for now so eh, if it becomes a problem refactor but it won't
            recursive_replace(x, find_text, replace_text)  # recurse

def replace_in_file(path, find_text, replace_text):
    # open file, read content, replace and write back
    pathname = str(path)
    if "replacement_script" in pathname:
        return  # skip self
    with path.open() as file:
        content = file.read()
    content = content.replace(find_text, replace_text)
    path.write_text(content)



# command line interface for recursive text replacement in python scripts
parser = argparse.ArgumentParser(description="replace text in a python script")
# file path
parser.add_argument("-fp", type=str, help="Path to the python script")
# recursive True/False
parser.add_argument("-r", type=bool, help="whether to go through all files in folder and sub folders recursively", default=False)
# text to find
parser.add_argument("-find", type=str, help="text to find")
# text to replace with
parser.add_argument("-replace", type=str, help="text to replace with")
args = parser.parse_args()
path = Path(args.fp)

if not path.exists():
    print(f"Path {path} does not exist")
    exit(1)

if args.r:
    recursive_replace(path, args.find, args.replace)
else:
    replace_in_file(path, args.find, args.replace)
