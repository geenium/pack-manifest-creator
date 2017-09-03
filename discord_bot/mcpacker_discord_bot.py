import logging
import discord
from discord.ext.commands import Bot
from os import remove, rename, getcwd
from shutil import make_archive
from uuid import uuid4 as new_uuid
from os import path as os_path

logging.basicConfig(level=logging.INFO)

mcpacker = Bot(command_prefix="!")

bot_token = #BOT TOKEN HERE

# Allows you to delete the bots messages, which the bot hasn't deleted itself
@mcpacker.command(pass_context=True)
async def delete(context):
    async for message in mcpacker.logs_from(context.message.channel, limit=25):
        if message.author == mcpacker.user:
            await mcpacker.delete_message(message)


# If the user cannot be DMed this message is sent to chat
async def no_dm(author):
    await mcpacker.say("I cannot DM you, {}\nPlease enable it in the \
privacy settings for this server".format(author))


def make_description(description):
    return '\n\t\t"description": "{}",'.format(" ".join(description))


# Creates and sends the mcpack
async def send_pack(context, data_type, name, description):
    # The description is a tuple of strings, from the end of the arguments
    description = " ".join(description)

    file = "manifest.json"
    with open(file, "w") as f:
        # Contents of the manifest for behaviour/resource packs
        contents = '{{\n\t"format_version": 1,\n\t"header": {{{}\
\n\t\t"name": "{}",\n\t\t"uuid": "{}",\n\t\t"version": [ 0, 0, 1 ]\n\t}},\
\n\t"modules": [\n\t\t{{\n\t\t\t"type": "{}",\n\t\t\t"uuid": "{}",\n\t\t\t\
"version": [ 0, 0, 1 ]\n\t\t}}\n\t]\n}}'
        f.write(contents.format(description, name, new_uuid(), data_type,
                                new_uuid()))

    # Creates a zipped folder and copies manifest.json inside
    make_archive(name, "zip", getcwd(), file)
    # Removes the old manifest.json copy
    remove(file)
    # Renames the zip file to .mcpack
    pack_name = name + ".mcpack"
    rename(name + ".zip", pack_name)

    # DMs the file straight to the user
    try:
        file = await mcpacker.send_file(context.message.author, pack_name)
        print(str(file))
        await mcpacker.add_reaction(file, "\u274c")
    # If the user does not accept DMs from people within the server
    # The file cannot be DMed and this message is displayed
    except discord.errors.Forbidden:
        await no_dm(context.message.author.mention)

    remove(name + ".mcpack")

    # Deletes the file when the :x: emoji is added as a reaction
    await mcpacker.wait_for_reaction(emoji="\u274c",
                                     user=context.message.author)
    await mcpacker.delete_message(file)


# Context is passed to get the user id of the person who activated the command
@mcpacker.group(pass_context=True)
async def mcpack(context):
    # If there is no subcommand ie "!mcpack" then the help message is sent
    if context.invoked_subcommand is None:
        try:
            await mcpacker.send_message(context.message.author,
"Use !mcpack <pack> <name> <description>\npack can be (resources, \
resource_pack, rp), (behaviors, behaviours, behavior_pack, behaviour_pack, bp)\
, or (skins, skin_pack, sp)")
        except discord.errors.Forbidden:
            await no_dm(context.message.author.mention)


# Subcommands of mcpack ie "!mcpack resources", "!mcpack behaviors"
@mcpack.command(pass_context=True, aliases=["resource_pack", "rp"])
async def resources(context, name, *description):
    await send_pack(context, "resources", name, make_description(description))


@mcpack.command(pass_context=True, aliases=["behaviours", "behavior_pack",
                                            "behaviour_pack", "bp"])
async def behaviors(context, name, *description):
    await send_pack(context, "data", name, make_description(description))


@mcpack.command(pass_context=True, aliases=["skin_pack", "sp"])
async def skins(context, name):
    await send_pack(context, "skin_pack", name, "")

mcpacker.run(bot_token)
