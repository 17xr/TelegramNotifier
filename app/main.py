"""
Made by @17xr

This script is a simple tool that sends a notification,
when you receive a private or a group Telegram message.

In order to use this tool, you should create a Telegram App,
for more information visit the following link:
"https://core.telegram.org/api/obtaining_api_id"

Don't forget to run " pip install -r requirements.txt" to install required dependencies.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from telethon.sync import TelegramClient, events
    from telethon.tl import types
    from plyer import notification

except ImportError:
    print("Error when importing dependencies")
    sys.exit(1)


def get_name(sender: types.User) -> str:
    """
    Get the name of the person who sent the message

    Args:
        sender (types.User): The sender Telethon object

    Returns:
        str: Name of the person who sent the message
    """

    f_name = sender.first_name
    l_name = sender.last_name
    name = ""
    if f_name is not None:
        name += f_name
    if l_name is not None:
        name += " " + l_name

    return name.strip()


def get_message(message: types.Message) -> str:
    """
    Get the message text

    Args:
        message (types.Message): Telethon Message object

    Returns:
        str: Message text
    """
    message = message.message

    return message.strip()


def get_time() -> str:
    """ Get current time
    Returns:
        _type_: Time of message reception
    """

    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")

    return current_time


def notifier(name: str, message: str, message_time: str, app_name: str, save: bool) -> notification:
    """
    Send a notification when a message is received

    Args:
        name (str): Name of the person who sent the message
        message (str): The message text
        message_time (str): Time of message reception
        app_name (str): Set to "Telegram", may change in the future
        save (bool): Check if to save message or not

    Returns:
        notification: Well, It's the reason why I made this script lol
    """

    current_directory = os.getcwd()

    # Check if the current OS is Windows (plyer library requires this to make a proper icon for the notification)
    if os.name == 'nt':
        extension = ".ico"
    else:
        extension = ".png"

    path_icon = current_directory + "/assets/" + app_name + extension
    title = f'Message sent by "{name}"'
    message = f"[{message_time}]: {message}"

    # Clear, it will send the notification
    notification.notify(title=title, message=message, app_name=app_name, app_icon=path_icon, toast=False)

    full_message = f"\033[1;35m\033[1mMessage:\n\033[1;37m{message}\n\033[1;35m\033[1mSent by: \033[1;37m{name} \033[1;35m\033[1mat {message_time}\n"
    print(full_message)

    if save:
        with open('Saved_Messages.txt', mode='a') as file:
            file.write('[NewMessage]\n')
            file.write(f'Message:\n{message}\nSent by: {name} at {time}\n\n')


def config_creator() -> None:
    """
       Create the user configuration when not found or corrupted
    """

    print("You will be promoted to configure your credentials\n")

    try:
        api_id = str(input("Enter your Telegram Api ID: "))
        api_hash = str(input("Enter your Telegram Api Hash: "))
        save = str(input("Do you want to save your messages in a separate file ? (yes/no): "))

        if save.strip().lower() in ["y", "yes"]:
            save = True
        else:
            save = False

        private = str(input("Do you want to receive messages only from private chats ? (yes/no): "))

        if private.strip().lower() in ["y", "yes"]:
            private = True
        else:
            private = False

    except ValueError:
        print("Please Enter a string... ")
        sys.exit(1)

    data = dict()
    data['api_id'] = api_id
    data['api_hash'] = api_hash
    data['save'] = save
    data['private'] = private

    with open('config.json', mode='w') as file:
        json.dump(data, file)


def main():
    """
       Run the script and check for config file
    """

    print("\033[32m\033[1mWelcome To: \033[0;31m🆃🅴🅻🅴🅶🆁🅰🅼 🅽🅾🆃🅸🅵🅸🅴🆁")
    print("\033[32m\033[1mMade by: \033[0;31m\033[1m@1.7x5\033[0m\n")

    print("\033[32m\033[1mChecking config file...")

    # Change directory
    directory = Path(__file__).parent.parent
    os.chdir(directory)

    # Check if the config file exists
    check = os.path.exists('config.json')
    time.sleep(1)

    if check:
        print("Config file found !")

    else:
        print("Config file not found !")
        config_creator()

    while True:

        try:
            with open('config.json', mode='r') as file:
                data = json.load(file)

            api_id = data['api_id']
            api_hash = data['api_hash']
            save = data['save']
            private = data['private']

            break

        except KeyError:
            print("\nHmmm... Required information were not found, you'll be promoted to create them again:")
            config_creator()

    with TelegramClient('name', api_id, api_hash) as client:
        print("Everything is working! We will notify you when something happens...\n")

        @client.on(events.NewMessage(incoming=True))
        async def handler(event):
            private_message = event.is_private
            app = "Telegram"

            if private and private_message:
                name = get_name(await event.get_sender())
                message = get_message(event.message)
                message_time = get_time()
                notifier(name, message, message_time, app, save)

            else:
                name = get_name(await event.get_sender())
                message = get_message(event.message)
                message_time = get_time()
                notifier(name, message, message_time, app, save)

        client.run_until_disconnected()


main()
