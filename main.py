"""This module is the entry point for the Action."""

import os
from pathlib import Path
from packaging.version import Version


class VersionNotUpdated(Exception):
    """The version number has not been updated or updated incorrectly."""


def get_file_contents(main_path: Path, branch_path: Path, app_path: Path) -> (str, str):
    """
    This function returns the contents of the main branch version and working branch version.
    :param app_path: Path to app version file
    :param main_path: Path to version on main
    :param branch_path: Path to version on working branch
    :return: Tuple of versions (main, branch)
    """
    with open(main_path / app_path, "r", encoding="utf-8") as main_file:
        main_contents = main_file.read()
    with open(branch_path / app_path, "r", encoding="utf-8") as branch_file:
        branch_contents = branch_file.read()
    return main_contents, branch_contents


def compare_app_version(main: str, branch: str, input_path: str) -> str:
    """
    This function compares the versions using the packaging library.
    It raises an error if the versions are stale or incorrect.
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


def compare_compose_version(branch_version: str, branch_path: Path, compose_path: str, app_path: str) -> str:
    """
    This function compares the versions using the packaging library.
    It raises an error if the versions don't match.
    :param branch_version: Version of app on branch
    :param branch_path: Path to branch
    :param compose_path: Path to compose
    :param app_path: Path to app version file
    :return: true if found
    """
    with open(branch_path / compose_path, "r", encoding="utf-8") as compose_file:
        compose_file_contents = compose_file.readlines()
    version_str = ""
    for line in compose_file_contents:
        if "image" in line:
            version_str = line.strip('\n').split(":")[-1]
            print(version_str)
            break
    if Version(branch_version) != Version(version_str):
        raise VersionNotUpdated(
            f"The version number in {compose_path} doesn't match the version in {app_path}."
            f"\nPlease update this."
        )
    return "true"


if __name__ == "__main__":
    APP_PATH = Path(os.environ.get("INPUT_APP_VERSION_PATH"))
    COMPOSE_PATH = os.environ.get("INPUT_DOCKER_COMPOSE_PATH")
    ROOT_PATH = Path(os.environ.get("GITHUB_WORKSPACE"))
    MAIN_PATH = ROOT_PATH / "main"
    BRANCH_PATH = ROOT_PATH / "branch"

    main_version, branch_version = get_file_contents(MAIN_PATH, BRANCH_PATH, APP_PATH)
    APP_UPDATED = compare_app_version(main_version, branch_version, str(APP_PATH))

    if COMPOSE_PATH:
        COMPOSE_PATH = Path(COMPOSE_PATH)
        COMPOSE_UPDATED = compare_compose_version(branch_version, BRANCH_PATH, str(COMPOSE_PATH), APP_UPDATED)
        GITHUB_ENV = os.getenv('GITHUB_ENV')
        with open(GITHUB_ENV, "a") as env:
            env.write("compose_updated=true")

    # Set the outputs variable to "true"
    # No need to check here as we expect only true returned
    GITHUB_ENV = os.getenv('GITHUB_ENV')
    with open(GITHUB_ENV, "a") as env:
        env.write("app_updated=true")
