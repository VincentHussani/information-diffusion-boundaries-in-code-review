# pylint: disable=redefined-outer-name
import subprocess
import os
import yaml
found_notebook = False

def get_changed_files():  # Uses githubs inbuilt functions to get changed files
    changed_files_json = subprocess.run(["git", "diff", "--name-only","HEAD^"], stdout=subprocess.PIPE, check=True)
    changed_files = changed_files_json.stdout.decode("utf-8").split("\n")
    return changed_files

def notebook_checker(file):
    if found_notebook is False and file["extension"] == ".ipynb":
                    subprocess.run(["pip","install","nbformat","matplotlib","numpy"],stdout=subprocess.PIPE,check=True)
                    found_notebook = True


def get_required_tests(changed_files, testable_file): # compares the files to the ones in the dependencies yaml file to see which needs to be tested
    tests_to_run = []
    for file in changed_files:
        base_name = os.path.basename(file)
        base_name = os.path.splitext(base_name)[0]

        if file.startswith("test/test_"):
            base_name = base_name.replace("test_","")

        for i in testable_file:

            if i["name"] == base_name:
                tests_to_run.append(i["name"]) #Found a file which is supposed to be tested
                notebook_checker(i)
            elif set(i["dependencies"]).intersection(tests_to_run) or base_name in i["dependencies"]:
                tests_to_run.append(i["name"]) #Found a file which depends on a tested file
                notebook_checker(i)


    return set(tests_to_run)


if __name__ == "__main__":
    testable_files = []
    with open("dependencies.yaml", encoding="utf-8") as file:
        testable_files = yaml.safe_load(file)
    changed_files = get_changed_files()
    tests_to_run = get_required_tests(changed_files, testable_files)
    existing_tests = []
    for test_file in tests_to_run:
        test_path = f"test/test_{test_file}.py"
        if os.path.exists(test_path):
            existing_tests.append(test_path)
    ALL_TEST = " ".join(existing_tests)
    print(ALL_TEST)
