"""
The main entry package for running CursorMaker, provides the CLI interface and handles launching the GUI when
available...
"""

from pathlib import Path
from lib import theme_util
import sys

# Attempt to import the gui, if it fails(gui packages missing) set the module to none to let methods below know...
try:
    from gui.cursorthememaker import launch_gui
except ImportError as e:
    print(repr(e))
    launch_gui = None

def print_help():
    """
    Print the usage info for CursorMaker to the command line.
    """
    print("Cursor Theme Maker")
    print("Usage:")
    print("No arguments: Launch the GUI")
    print("'--help': Display help")
    print("'--build FILE1 FILE2 ...': Build cursor projects from the command line \n"
          "by passing the json files of the projects...")
    print("'--open FILE': Open the specified cursor project in the GUI by providing the json file...")
    # TODO: print("'--convert INPUT_FILE OUTPUT_FILE FORMAT': Convert")

def main(args):
    """
    Main method of the cursor maker program. Parses the first flag and figures out what to do based on it...

    :param args: List of user passed arguments.
    """
    if(len(args) == 0):
        # No arguments, launch the gui if possible
        if(launch_gui is not None):
            launch_gui(None)
        else:
            print("Unable to import and run gui, check if PySide2 is installed...")
            print_help()
        return

    # --help, print the help info...
    if(args[0] == "--help"):
        print_help()
    # --open, grab next argument, and attempt to have gui open it...
    elif(args[0] == "--open"):
        if(len(args) > 1):
            if(launch_gui is not None):
                launch_gui(args[1])
            else:
                print("Unable to import and run gui, check if PySide2 is installed...")
        else:
            print("No file provided...")
            launch_gui(None)
    # --build, load in the project file and build the theme in place using utils api...
    elif(args[0] == "--build"):
        for config_file in args[1:]:
            try:
                config_path = Path(config_file)
                metadata, fc_data = theme_util.load_project(config_path)
                fc_data = {name: cursor for name, (cur_path, cursor) in fc_data.items()}
                theme_util.build_theme(config_path.parent.name, config_path.parent.parent, metadata, fc_data)
            except Exception as e:
                print(e)
                raise e
        print("Build Successful!")
    else:
        # Rogue arguments or flags passed, just print help...
        print_help()


if(__name__ == "__main__"):
    main(sys.argv[1:])