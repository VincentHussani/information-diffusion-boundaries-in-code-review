# pylint: disable=redefined-outer-name
import subprocess
import os
import yaml


def get_changed_files():  # Uses githubs inbuilt functions to get changed files
    changed_files_json = subprocess.run(["git", "diff", "--name-only","HEAD^"], stdout=subprocess.PIPE, check=True)
    changed_files = changed_files_json.stdout.decode("utf-8").split("\n")
    return changed_files


def get_required_tests(changed_files, dependencies): # compares the files to the ones in the dependencies yaml file to see which needs to be tested
    has_notebooks =False
    tests_to_run = []
    for file in changed_files:
        if file.startswith("test/test_") :
            test_name = os.path.basename(file).replace("test_", "")
            test_name = test_name.replace(".py","")
            tests_to_run.append(test_name)
            # If the test file is for a notebook, convert the notebook to Python
            # if not has_notebooks:
            #     corresponding_notebook = next((dep for dep in dependencies if dep["name"] == test_name and dep["extension"] == ".ipynb"), None)
            #     if corresponding_notebook:
            #         has_notebooks = True
            #         subprocess.run(["pip", "install", "nbclient", "nbformat"], check=True)
            for i in dependencies:
                if set(i["dependencies"]).intersection(set(tests_to_run)):
                    tests_to_run.append(i["name"])
        else :
            for i in dependencies:
                full_path = i["path"] + i["name"] + i["extension"]
                if full_path == file:
                    tests_to_run.append(i["name"])
                elif set(i["dependencies"]).intersection(set(tests_to_run)):
                    tests_to_run.append(i["name"])
            # if not has_notebooks and file.endswith(".ipynb"):
            #     has_notebooks = True
            #     subprocess.run(["pip", "install", "nbclient", "nbformat"], check=True)
    return set(tests_to_run)


if __name__ == "__main__":
    dependencies = []
    with open("dependencies.yaml", encoding="utf-8") as file:
        dependencies = yaml.safe_load(file)
    changed_files = get_changed_files()
    tests_to_run = get_required_tests(changed_files, dependencies)

    tests_to_run = get_required_tests(changed_files, dependencies)
    all_tests = " ".join(f"test/test_{test_file}.py" for test_file in tests_to_run)
    print(all_tests)
