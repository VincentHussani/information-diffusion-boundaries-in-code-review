# pylint: disable=redefined-outer-name
import os
import yaml
from get_tests import notebook_checker, get_changed_files

def get_required_tests(changed_files, testable_file): # compares the files to the ones in the dependencies yaml file to see which needs to be tested
    tests_to_run = []
    found_notebook = False

    for file in changed_files:
        base_name = os.path.basename(file)
        base_name = os.path.splitext(base_name)[0]

        if file.startswith("test/test_"):
            base_name = base_name.replace("test_","")

        for i in testable_file:
            if i["test_with_orjson"] and i["name"] == base_name:
                tests_to_run.append(i["name"]) #Found a file which is supposed to be tested
                found_notebook = notebook_checker(i,found_notebook)

            elif i["test_with_orjson"] and set(i["dependencies"]).intersection(tests_to_run) or base_name in i["dependencies"]:
                tests_to_run.append(i["name"]) #Found a file which depends on a tested file
                found_notebook = notebook_checker(i,found_notebook)
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
