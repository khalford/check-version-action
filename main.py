import os
from pathlib import Path


ROOT_PATH = Path(os.environ.get('GITHUB_WORKSPACE'))
MAIN_PATH = ROOT_PATH / "main"
BRANCH_PATH = ROOT_PATH / "branch"
INPUT_PATH = Path(os.environ.get('INPUT_PATH'))

def get_file_contents():
    print(os.listdir(ROOT_PATH))





if __name__ == '__main__':
    get_file_contents()
