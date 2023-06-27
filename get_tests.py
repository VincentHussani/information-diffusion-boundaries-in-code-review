# pylint: disable=redefined-outer-name
import logging
import subprocess
import os
import yaml

logging.basicConfig(filename='get_tests.log', level=logging.DEBUG)
def convert_notebook(notebook: str):
    new_path = notebook.replace(".ipynb", ".py")
    subprocess.run(["jupyter", "nbconvert", "--to", "script", notebook], check=True)
    return new_path

def get_changed_files():  # Uses githubs inbuilt functions to get changed files
    changed_files_json = subprocess.run(
        ["git", "diff", "--name-only","HEAD^"], stdout=subprocess.PIPE, check=True
    )
    changed_files = changed_files_json.stdout.decode("utf-8").split("\n")
    logging.debug(f"Changed files: {changed_files}")  # Debug log
    return changed_files



def get_required_tests(
    changed_files, dependencies
):  # compares the files to the ones in the dependencies yaml file to see which needs to be tested
    tests_to_run = []
    for file in changed_files:
        if file.startswith("test/test_") :
            test_name = os.path.basename(file).replace("test_", "")
            test_name = test_name.replace(".py","")
            tests_to_run.append(test_name+".py")
            # If the test file is for a notebook, convert the notebook to Python
            corresponding_notebook = next((dep for dep in dependencies if dep["name"] == test_name and dep["extension"] == ".ipynb"), None)
            if corresponding_notebook:
                logging.debug("We in :)")  # Debug log
                convert_notebook(corresponding_notebook["path"] + corresponding_notebook["name"] + corresponding_notebook["extension"])
        else:
            for i in dependencies:
                full_path = i["path"] + i["name"] + i["extension"]
                if full_path == file:
                    tests_to_run.append(i["name"])
                elif set(i["dependencies"]).intersection(set(tests_to_run)):
                    tests_to_run.append(i["name"])
            if file.endswith(".ipynb"):
                convert_notebook(file)
    logging.debug(f"Tests to run: {tests_to_run}")  # Debug log
    return set(tests_to_run)


if __name__ == "__main__":
    dependencies = []
    with open("dependencies.yaml", encoding="utf-8") as file:
        dependencies = yaml.safe_load(file)
    changed_files = get_changed_files()
    tests_to_run = get_required_tests(changed_files, dependencies)

    tests_to_run = get_required_tests(changed_files, dependencies)
    all_tests = " ".join(f"test/test_{test_file}" for test_file in tests_to_run)
    print(all_tests)
