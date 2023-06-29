# pylint: disable=redefined-outer-name
import subprocess
import os
import yaml


def get_changed_files():  # Uses githubs inbuilt functions to get changed files
    changed_files_json = subprocess.run(["git", "diff", "--name-only","HEAD^"], stdout=subprocess.PIPE, check=True)
    changed_files = changed_files_json.stdout.decode("utf-8").split("\n")
    return changed_files


def get_required_tests(changed_files, dependencies): # compares the files to the ones in the dependencies yaml file to see which needs to be tested
    tests_to_run = []

    for file in changed_files:
        base_name = os.path.basename(file)
        base_name = os.path.splitext(base_name)[0]

        if file.startswith("test/test_"):
            base_name.replace("test_","")

        for i in dependencies:
            if i["name"] == base_name:
                tests_to_run.append(i["name"]) #Found a file which is supposed to be tested
                if i["extension"] == ".ipynb":
                    pass
            elif set(i["dependencies"]).intersection(tests_to_run) or base_name in i["dependencies"]:
                tests_to_run.append(i["name"]) #Found a file which depends on a tested file
                if i["extension"] == ".ipynb":
                    pass
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
