from uuid import uuid4 as new_uuid
from os import path as os_path, makedirs, sep, getenv, listdir, chdir, getcwd


# Writes the manifest
def create_manifest(path):
    with open(path, "w") as f:
        f.write(contents.format(name, new_uuid(), manifest_type, new_uuid(),
                                desc=description))
        # Prints a success message
        print(name, "{} pack manifest successfully created!".format(
        input_type))

# Gets the original directory incase Winodws 10 Minecraft isn't installed
original = getcwd()
# Moves to C://.../appdata/Local/Packages
# This is where the data for Win10 Minecraft is located
chdir(sep.join(getenv("appdata").split(sep)[:-1]) +
      "{s}Local{s}Packages".format(s=sep))

# Goes into the correct folder, which begins with Microsoft.MinecraftUWP
changed = False
for i in listdir():
    if i[:22] == "Microsoft.MinecraftUWP":
        changed = True
        chdir(i)
        break

# This will trigger if Win10 Minecraft isn't installed
if not changed:
    print("Windows 10 Minecraft not found...\nFolders will be created at \
python script's location")
    chdir(original)
# Moves to the folder where behaviour/resource packs are located
else:
    # Asks whether a resourcepack or behaviour pack should be made
    pack = input("Do you want a resource pack or behaviour pack (r/b)?\n>> ")
    # Only accepts 'r' or 'b' as input
    while pack != "r" and pack != "b":
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
    folder_type = input_type + "_packs"
    # Changes to the correct directory
    # Either the behaviour packs folder OR resourcepacks folder
    chdir("LocalState{s}games{s}com.mojang{s}{}".format(folder_type, s=sep))

# Contents of the manifest for behaviour/resource packs
contents = """{{
    "format_version": 1,
    "header": {{
        "description": "{desc}",
        "name": "{}",
        "uuid": "{}",
        "version": [ 0, 0, 1 ]
    }},
    "modules": [
        {{
            "description": "{desc}",
            "type": "{}",
            "uuid": "{}",
            "version": [ 0, 0, 1 ]
        }}
    ]
}}"""

# Gets the name and description for the behaviour/resource pack
name = input("What is the name of the {} pack?\n>> ".format(input_type))
description = input("What will the description for the {} pack be?\
\n>> ".format(input_type))

# If the path doesn't exist there isn't anything to overwrite
if not os_path.exists(name):
    # Creates a new folder
    makedirs(name)
    # Writes the manifest file
    create_manifest(name + sep + "manifest.json")
# Stops the program from automatically overwriting existing manifests
else:
    overwrite = input("{} pack with same name already exists.\n\
Overwrite existing manifest? y/n\n>> ".format(input_type.title())).lower()
    # Only accepts 'y' or 'n' as a valid input
    while overwrite != "y" and overwrite != "n":
        overwrite = input("Please enter 'y' or 'n'\n>> ")
    if overwrite == "y":
        create_manifest(name + sep + "manifest.json")
    # If the existing manifest doesn't want to be overwritten
    # Prints unsuccessful message
    else:
        print("New manifest not created...")

# Allows people to see success or unsuccessful messages before exiting
input("Press 'enter' to finish...")
