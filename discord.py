"""
This plugin will link GNAT Studio to Discord using Rich Presence.

It will show what you are currently doing on the IDE (which file you are editing/viewing).
It will also show which project you are working on.

Made by Shinyhero36: https://github.com/Shinyhero36
"""

#############################################################################
# No user customization below this line
#############################################################################
# noinspection PyPackageRequirements
import GPS

from rpc import DiscordIpcClient
from time import time

CLIENTID = ""
discord = DiscordIpcClient.for_platform(CLIENTID)  # Send the client ID to the rpc module

now = time()


# noinspection PyTypeChecker
def update(project_name=None, filename=None):
    """
    Update Discord Rich Presence

    Args:
        project_name (str): Self Explanatory
        filename (str): Self Explanatory

    Returns:
        Returns an updated rich presence
    """
    if project_name:
        activity = {
            "details": project_name,
            "timestamps": {
                "start": round(now)
            },
            "assets": {
                "large_image": "gnat",
            }
        }

        if filename:
            activity["state"] = filename
            activity["assets"]["large_text"] = "{} - {}".format(project_name, filename)
        else:
            activity["assets"]["large_text"] = project_name

        # print("Setting activity:")
        # for k, v in activity.items():
        #     print("-> {} {}".format(k, v))
        discord.set_activity(activity)


# noinspection PyUnusedLocal
def on_context_changed(name, context):
    """
    Emitted when the current context changes in GPS, such as when a new file or entity is selected, or a window is
    created

    Args:
        name (str): Hook name
        context (GPS.Context): Context

    """
    try:
        project_name = context.file().project().name()
        file_name = context.file().base_name()

        update(project_name, "Editing " + file_name)
    except AttributeError as e:
        return


# noinspection PyUnusedLocal
def on_gps_started(name):
    """
    Emitted when GPS is fully loaded and its window is visible to the user.

    Args:
        name (str): Hook name

    Returns:

    """
    update("Idling...")


GPS.Hook("gps_started").add(on_gps_started)
GPS.Hook("context_changed").add(on_context_changed)
