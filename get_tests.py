# pylint: disable=redefined-outer-name
import subprocess
import os
import yaml


def convert_notebook(notebook: str):
    new_path = notebook.replace(".ipynb", ".py")
    subprocess.run(["jupyter", "nbconvert", "--to", "script", notebook], check=True)
    return new_path

def get_changed_files():  # Uses githubs inbuilt functions to get changed files
    changed_files_json = subprocess.run(
        ["git", "diff", "--name-only","HEAD^"], stdout=subprocess.PIPE, check=True
    )
    return changed_files_json.stdout.decode("utf-8").split("\n")



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

    tests_to_run = get_required_tests(changed_files, dependencies)
    all_tests = " ".join(f"test/{test_file}_test.py" for test_file in tests_to_run)
    print(all_tests)
