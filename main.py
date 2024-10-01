import os
import sys
from pathlib import Path

try:
    if sys.argv[1] == "local":
        MAIN_PATH = Path("./main_version")
        BRANCH_PATH = Path("./branch_version")
except IndexError:
    INPUT_PATH = Path(os.environ.get('INPUT_PATH'))
    ROOT_PATH = Path(os.environ.get('GITHUB_WORKSPACE'))
    MAIN_PATH = ROOT_PATH / "main" / INPUT_PATH
    BRANCH_PATH = ROOT_PATH / "branch" / INPUT_PATH


class VersionNotUpdated(Exception):
    """The version number has not been updated."""


def get_file_contents():
    with open(MAIN_PATH, "r") as main:
        main_contents = main.read()
    with open(BRANCH_PATH, "r") as branch:
        branch_contents = branch.read()
    return main_contents, branch_contents


def compare(main, branch):
    main_split = main.split(".")
    branch_split = branch.split(".")
    print(f"Main Version is: {main_split}")
    print(f"Branched Version is: {branch_split}")
    for i in range(3):
        if main_split[i] != branch_split[i]:
            return True
    raise VersionNotUpdated(f"The version number in {INPUT_PATH} has not been updated."
                            f"\nPlease update this following semver convention")


if __name__ == '__main__':
    main_content, branch_content = get_file_contents()
    updated = compare(main_content, branch_content)
    print(f"::set-output name=updated::{updated}")
