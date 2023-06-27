# pylint: disable=redefined-outer-name
import subprocess
import os
import yaml


def convert_notebook(notebook: str):
    new_path = notebook.replace(".ipynb", ".py")
    subprocess.run(["jupyter", "nbconvert", "--to", "script", notebook], check=True)
    return new_path


def get_changed_files():  # Uses githubs inbuilt functions to get changed files
    try:
        commit_range = subprocess.check_output(['git', 'rev-list', '--max-parents=0', 'HEAD^..HEAD'], encoding='utf-8').strip()
        changed_files_json = subprocess.run(["git", "diff", "--name-only", commit_range], stdout=subprocess.PIPE, check=True)
        return changed_files_json.stdout.decode('utf-8').split('\n')
    except subprocess.CalledProcessError:
        # Handle the case where the commit range is invalid or there is no commit history
        return []


def get_required_tests(
    changed_files, dependencies
):  # compares the files to the ones in the dependencies yaml file to see which needs to be tested
    tests_to_run = []
    for file in changed_files:
        if file.startswith("test/") and file.endswith("_test.py"):
            tests_to_run.append(os.path.basename(file).replace("_test.py", ""))
        else:
            for i in dependencies:
                full_path = i["path"] + i["name"] + i["extension"]
                if full_path == file:
                    tests_to_run.append(i["name"])
                elif set(i["dependencies"]).intersection(set(tests_to_run)):
                    tests_to_run.append(i["name"])
            if file.endswith(".ipynb"):
                convert_notebook(file)
    return set(tests_to_run)


if __name__ == "__main__":
    dependencies = []
    with open("dependencies.yaml", encoding="utf-8") as file:
        dependencies = yaml.safe_load(file)
    changed_files = get_changed_files()
    tests_to_run = get_required_tests(changed_files, dependencies)

    for (
        test_file
    ) in (
        tests_to_run
    ):  # this is used to print out the names of the tests to be conducted in a file to be later read by the CI :)
        print(f"test/{test_file}_test.py")
