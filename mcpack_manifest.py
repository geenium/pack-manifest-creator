from uuid import uuid4 as new_uuid
from os import path as os_path, makedirs, sep, getenv, listdir, chdir, getcwd


# Writes the manifest
def create_manifest(path):
    with open(path, "w") as f:
        f.write(contents.format(name, new_uuid(), new_uuid(),
                                desc=description))
        # Prints a success message
        print(name, "behaviour pack manifest successfully created!")

# Gets the original directory incase Winodws 10 Minecraft isn't installed
original = getcwd()
# Moves to C://.../appdata/Local/Packages
# This is where the data for Win10 Minecraft is located ie behaviour packs
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
# Moves to the folder where behaviour packs are located
else:
    chdir("LocalState{s}games{s}com.mojang{s}behavior_packs".format(s=sep))

# Contents of the manifest for behaviour packs
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
            "type": "data",
            "uuid": "{}",
            "version": [ 0, 0, 1 ]
        }}
    ]
}}"""

# Gets the name and description for the behaviour pack
name = input("What is the name of the behaviour pack?\n>> ")
description = input("What will the description for the behaviour pack be?\
\n>> ")

# If the path doesn't exist there isn't anything to overwrite
if not os_path.exists(name):
    # Creates a new folder
    makedirs(name)
    # Writes the manifest file
    create_manifest(name + sep + "manifest.json")
# Stops the program from automatically overwriting existing manifests
else:
    overwrite = input("Behaviour pack with same name already exists.\n\
Overwrite existing manifest? y/n\n>> ").lower()
    # Only accepts 'y' or 'n' as a valid input
    while overwrite != "y" and overwrite != "n":
        overwrite = input("Please enter 'y' or 'n'\n>> ")
    if overwrite == "y":
        create_manifest(name + sep + "manifest.json")
    # If the existing manifest doesn't want to be overwritten
    # Prints Unsuccessful message
    else:
        print("New manifest not created...")

# Allows people to see success or unsuccessful messages before exiting
input("Press 'enter' to finish...")
