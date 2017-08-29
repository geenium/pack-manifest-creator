from os import makedirs, getenv, listdir, chdir, getcwd, remove, rename
from shutil import make_archive
from uuid import uuid4 as new_uuid
from os import path as os_path


# Only accepts 'y' or 'n' as an input
def yes_no(variable):
    while variable not in ["y", "n"]:
        variable = input("Please enter 'y' or 'n'\n>> ").lower()
    if variable == "y":
        return True
    return False


# Writes the manifest
def create_manifest(name, data_type, description):
    file = "manifest.json"
    with open(file, "w") as f:
        # Contents of the manifest for behaviour/resource packs
        contents = '{{\n\t"format_version": 1,\n\t"header": {{\
\n\t\t"description": "{}",\n\t\t"name": "{}",\n\t\t"uuid": "{}",\
\n\t\t"version": [ 0, 0, 1 ]\n\t}},\n\t"modules": [\n\t\t{{\
\n\t\t\t"type": "{}",\n\t\t\t"uuid": "{}",\n\t\t\t"version": [ 0, 0, 1 ]\
\n\t\t}}\n\t]\n}}'
        f.write(contents.format(description, name, new_uuid(), data_type,
                                new_uuid()))

    # Creates a zipped folder and copies manifest.json inside
    make_archive(name, "zip", getcwd(), file)
    # Removes the old manifest.json copy
    remove(file)
    # Renames the zip file to .mcpack
    if os_path.exists(name + ".mcpack"):
        num = 1
        while os_path.exists(name + str(num) + ".mcpack"):
            num += 1
        rename(name + ".zip", name + str(num) + ".mcpack")
    else:
        rename(name + ".zip", name + ".mcpack")

    # Prints a success message
    print("New {} pack manifest successfully created!\n".format(data_type))


# Creates the zip folder for new resourcepacks and behaviour packs
def new_manifest():
    # Asks whether a resourcepack or behaviour pack should be made
    pack = input("Do you want a resource pack or behaviour pack? (r/b)\n\
>> ")

    # Only accepts 'r' or 'b' as input
    while pack not in ["r", "b"]:
        pack = input("Please enter 'r' for resource pack or 'b' for \
behaviour pack!\n>> ")

    # Sets certain values for resourcepacks
    if pack == "r":
        input_type = "resource"
        manifest_type = "resources"
    # Sets certain values for behaviour packs
    else:
        input_type = "behavior"
        manifest_type = "data"

    # Gets the name and description for the behaviour/resource pack
    name = input("What is the name of the {} pack?\n>> ".format(input_type))

    description = input("What will the description for the {} pack be?\
\n>> ".format(input_type))

    create_manifest(name, manifest_type, description)

# Asks if a new pack should be created, if not the program stops
while yes_no(input("Do you want to create a new pack? (y/n)\n>> ").lower()):
    new_manifest()
