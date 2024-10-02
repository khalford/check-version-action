"""This module is the entry point for the Action."""

import os
import json
from pathlib import Path
from packaging.version import Version


class VersionNotUpdated(Exception):
    """The version number has not been updated or updated incorrectly."""


def get_file_contents(main_path: Path, branch_path: Path) -> (str, str):
    """
    This function returns the contents of the main branch version and working branch version.
    :param main_path: Path to version on main
    :param branch_path: Path to version on working branch
    :return: Tuple of versions (main, branch)
    """
    with open(main_path, "r", encoding="utf-8") as main_file:
        main_contents = main_file.read()
    with open(branch_path, "r", encoding="utf-8") as branch_file:
        branch_contents = branch_file.read()
    return main_contents, branch_contents


def compare(main: str, branch: str, input_path: str) -> str:
    """
    This function compares the versions using the packaging library.
    It raises an error is the versions are stale or incorrect.
    :param main: Version on main
    :param branch: Version on working branch
    :param input_path: Path to version file to display in error
    :return: Returns "true" to follow GitHub Actions bools
    """
    if Version(branch) <= Version(main):
        raise VersionNotUpdated(
            f"The version number in {input_path} has not been updated or updated incorrectly."
            f"\nPlease update this following semver convention."
        )
    return "true"


if __name__ == "__main__":
    INPUT_PATH = Path(os.environ.get("INPUT_PATH"))
    ROOT_PATH = Path(os.environ.get("GITHUB_WORKSPACE"))
    MAIN_PATH = ROOT_PATH / "main" / INPUT_PATH
    BRANCH_PATH = ROOT_PATH / "branch" / INPUT_PATH

    main_version, branch_version = get_file_contents(MAIN_PATH, BRANCH_PATH)
    UPDATED = compare(main_version, branch_version, INPUT_PATH)
    # Set the outputs variable to "true"
    # No need to check here as we expect only true returned
    print(f"::set-output name=updated::{UPDATED}")
    github_output = json.loads(os.environ.get("GITHUB_OUTPUT"))
    github_output["updated"] = UPDATED
    os.environ["GITHUB_OUTPUT"] = github_output.dumps()
