from uuid import uuid4 as new_uuid
from os import path as os_path, makedirs, sep, getenv, listdir, chdir, getcwd
from shutil import copytree, copy


# Only accepts 'y' or 'n' as an input
def yes_no(variable):
    while variable not in ["y", "n"]:
        variable = input("Please enter 'y' or 'n'\n>> ").lower()
    if variable == "y":
        return True
    return False


# Function which copies the textures to the pack
def get_assets(ask, folder, pack):
    if yes_no(input("Do you want the {}? (y/n)\n>> ".format(ask)).lower()):
        print("Extracting...\n")
        try:
            copytree(folder, pack + folder)
        except FileExistsError:
            print("That can't be extracted as the folder already exists!")
        except NotADirectoryError:
            copy(folder, pack + folder)


# Writes the manifest
def create_manifest(path, name, data_type, description):
    with open(path, "w") as f:
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
        f.write(contents.format(name, new_uuid(), data_type, new_uuid(),
                                desc=description))
        # Prints a success message
        print("New {} pack manifest successfully created!\n".format(
              data_type))


# Extracts the default assets specified
def extract(pack_type, pack_loc):
    chdir(getenv("programw6432") + sep + "WindowsApps")
    for d in listdir():
        if d[:22] == "Microsoft.MinecraftUWP":
            chdir("{}{s}data{s}{}_packs{s}vanilla".format(d, pack_type, s=sep))
            break
    if pack_type == "resource":
        # Checks which types of assets want to be extracted
        # Mob models
        get_assets("mob models", "models", pack_loc)

        if not os_path.exists(pack_loc + sep + "textures"):
            # Changes directory for easy extraction of textures
            makedirs(pack_loc + sep + "textures")
        chdir("textures")
        pack_loc += "textures" + sep

        # Gets armour textures if needed
        chdir("models")
        get_assets("armour textures", "armor", pack_loc + "models" + sep)
        chdir("..")

        # List of textures and the folders they are in
        textures_to_get = [["block textures", "blocks"],
                           ["colormaps", "colormap"],
                           ["entity textures", "entity"],
                           ["environment textures", "environment"],
                           ["gui textures", "gui"],
                           ["item textures", "items"],
                           ["map textures", "map"],
                           ["misc textures", "misc"],
                           ["paintings", "painting"],
                           ["particle textures", "particle"],
                           ["flame texture", "flame_atlas.png"],
                           ["worldborder texture", "forcefield_atlas.png"]]

        for t in textures_to_get:
            # Passes each list inside the list to get_assets
            get_assets(*t, pack_loc)

    else:
        behaviours_to_get = [["entity behaviours", "entities"],
                             ["loot tables", "loot_tables"],
                             ["villager trades", "trading"]]

        for b in behaviours_to_get:
            # Passes each list inside the list to get_assets
            get_assets(*b, pack_loc)

    print("All assets that could/you wanted to be extracted have been.")


# Creates the folder for new resourcepacks and behaviour packs
def new_manifest(installed):
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

    if installed:
        chdir(input_type + "_packs")

    # Gets the name and description for the behaviour/resource pack
    name = input("What is the name of the {} pack?\n>> ".format(input_type
                                                                ))

    description = input("What will the description for the {} pack be?\
\n>> ".format(input_type))

    # If the file doesn't exist there isn't anything to overwrite
    if not os_path.exists(name):
        makedirs(name)
        # Writes the manifest file
        create_manifest(name + sep + "manifest.json", name, input_type,
                        description)
    # Stops the program from automatically overwriting existing manifests
    else:
        if yes_no(input("{} pack with same name already exists.\nOverwrite \
existing manifest? (y/n)\n>> ".format(input_type.title())).lower()):
            create_manifest(name + sep + "manifest.json", name, input_type,
                            description)
        # If the existing manifest doesn't want to be overwritten
        # Prints unsuccessful message
        else:
            print("New manifest not created...")
            changed = False
    # If not changed then windows 10 Minecraft isn't installed and the default
    # Assets will not be able to be extracted
    if installed:
        # Checks if some default assets should be installed into the resource
        # or behaviour pack to be changed later
        if yes_no(input("Would you like to extract some default assets? (y/n)\
\n>> ").lower()):
            pack_path = getcwd() + sep + name + sep

            print("\nNote: Extracting the assets can take some time.\n\
Please be patient while it works.\nAlso note textures cannot be extracted if \
the folder already exists in the pack.\n")
            extract(input_type, pack_path)

        else:
            print("Default assets have not been extracted.")

# # # # # # # # # # # # # # # # # #
# This is where the script begins #
# # # # # # # # # # # # # # # # # #

# Gets the original directory in case Winodws 10 Minecraft isn't installed
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
        chdir(i + sep + "LocalState{s}games{s}com.mojang".format(s=sep))
        break

# This will trigger if Win10 Minecraft isn't installed
if not changed:
    print("Windows 10 Minecraft not found...\nFolders will be created at \
python script's location")
    chdir(original)

# Asks if a new pack should be created, if not the program stops
if yes_no(input("Do you want to create a new pack? (y/n)\n>> ").lower()):
    new_manifest(changed)

# Allows people to see success or unsuccessful messages before exiting
input("Press 'enter' to finish...")
