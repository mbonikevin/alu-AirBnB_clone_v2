#!/usr/bin/python3
"""
HBNBCommand Module
===================
Module: command-line interpreter (CLI) for the Holberton BNB project.
It uses the `cmd` module to:
    -create an interactive shell for managing application objects.

Features:
# - Tab completion for commands.
# - Command history using the readline module.
- Object creation, display, deletion, and more.

Classes:
    - HBNBCommand: Defines the command-line interface.
"""

import cmd
import readline
import rlcompleter
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


# Enable tab completion
readline.parse_and_bind("tab: complete")

# Command history setup
HISTORY_FILE = ".cmd_history"

try:
    # Load command history if it exists
    readline.read_history_file(HISTORY_FILE)
except FileNotFoundError:
    pass  # No history file found, proceed silently

# valid classes
CLASSES = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review,
}


def inform_user_given_one_arg(arg):
    """
    Inform the user about missing or invalid arguments.

    Args:
        arg (str): The argument provided by the user.

    Prints:
        - "** class name missing **" if no argument is provided.
        - "** class doesn't exist **" if the class name is invalid.
        - "** instance id missing **" for incomplete commands.
    """
    if arg == "":
        print("** class name missing **")
    elif arg not in CLASSES.keys():
        print("** class doesn't exist **")
    else:
        print("** instance id missing **")


def inform_user_given_two_arg(class_name):
    """
    Inform the user about invalid or missing instances.

    Args:
        class_name (str): The class name provided by the user.

    Prints:
        - "** class doesn't exist **" if the class name is invalid.
        - "** no instance found **" if the instance doesn't exist.
    """
    if class_name not in CLASSES.keys():
        print("** class doesn't exist **")
    else:
        print("** no instance found **")


class HBNBCommand(cmd.Cmd):
    """
    Command-line interface for managing Holberton BNB objects.

    Attributes:
        prompt (str): The command prompt displayed to the user.
    """

    prompt = "(hbnb) "
    # dict of Classes
    _Classes = CLASSES.copy()
    # list of classes
    classes = CLASSES.keys()

    def do_quit(self, arg):
        """
        Exits the program.

        Args:
            arg (str): Optional argument (not used).

        Usage:
            quit
        """
        print("Have a Good Day!")
        return True

    def do_EOF(self, arg):
        """
        Exits the program when EOF is encountered.

        Args:
            arg (str): Optional argument (not used).

        Usage:
            EOF (press Ctrl+D)
        """
        return True

    def emptyline(self):
        """
        Prevents the shell from repeating the last command on an empty line.

        Returns:
            False: Ensures the prompt is displayed again.
        """
        return False

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel and saves it to storage.

        Args:
            # to be edited

        Usage:
            # to be edited
        """

        # test if class_name provided
        try:
            cls_name = arg.split()[0]
        except IndexError:
            print("** Class name missing **")
            return False

        if cls_name.istitle() and cls_name in self._Classes.keys():
            # create a dictionary to store parameters
            param_dict = {}
            if len(arg.split()) > 1:
                for arg in arg.split()[1:]:
                    if "=" in arg:
                        parts = arg.split("=")
                        try:
                            parts[1] = int(parts[1])
                        except ValueError:
                            try:
                                parts[1] = float(parts[1])
                            except ValueError:
                                parts[1] = parts[1].replace("_", " ")[1:-1]
                        param_dict[parts[0]] = parts[1]

            # class creation
            instance = (
                self._Classes[cls_name](**param_dict)
                if param_dict
                else self._Classes[cls_name]()
            )
            instance.save()
            print(instance.id)
        else:
            print("** class name doesn't exist")

    def do_show(self, arg):
        """
        Displays the string representation of an object.

        Args:
            arg (str): The class name and ID separated by a space.

        Usage:
            show <BaseModel or User or City
                or Amenity or Place or Review> + <id>
        """
        try:
            class_name, id = arg.split()
            all_objs = storage.all()
            key = ".".join([class_name, id])
            if key in all_objs.keys():
                print(all_objs[key])
            else:
                inform_user_given_two_arg(class_name)
        except ValueError:
            inform_user_given_one_arg(arg)

    def do_destroy(self, arg):
        """
        Deletes an object from storage.

        Args:
            arg (str): The class name and ID separated by a space.

        Usage:
            destroy <BaseModel or User or City
                    or Amenity or Place or Review> + <id>
        """
        try:
            class_name, id = arg.split()
            all_objs = storage.all()
            key = ".".join([class_name, id])
            if key in all_objs.keys():
                storage.delete(key)
            else:
                inform_user_given_two_arg(class_name)
        except ValueError:
            inform_user_given_one_arg(arg)

    def do_all(self, arg):
        """
        Displays all objects in storage or all objects of a specific class.

        Args:
            arg (str): The class name (optional).

        Usage:
            all [BaseModel, etc]
        """
        if arg in self.__class__.classes or arg == "":
            if arg:
                all_objs = storage.all(self._Classes[arg])
            else:
                all_objs = storage.all()
            all_list = []
            for key in all_objs.keys():
                if arg in self.__class__.classes:
                    if str(key).startswith(arg):
                        all_list.append(str(all_objs[key]))
                else:
                    all_list.append(str(all_objs[key]))
            print(all_list)
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """
        Updates an object's attributes.

        Args:
            arg (str): The class name, ID, attribute name, and value.

        Usage:
            update <class name> <id> <attribute name> <attribute value>
        """

        try:
            class_name, id, attr_name, attr_value = arg.split()
            all_objs = storage.all()
            key = ".".join([class_name, id])
            if class_name in self.__class__.classes and key in all_objs.keys():
                instance = all_objs[key]
                setattr(instance, attr_name, attr_value)
                instance.save()
            elif class_name in self.__class__.classes:
                print("** no instance found **")
            else:
                print("** class doesn't exist **")
        except ValueError:
            # when some values are missing
            args = len(arg.split())  # arguments 'args' after spliting input
            if arg == "":
                print("** class name missing **")
            elif args == 1 and arg.split()[0] in self.__class__.classes:
                print("** instance id missing **")
            elif arg.split()[0] not in self.__class__.classes:
                print("** class doesn't exist **")
            elif args == 2:
                print("** attribute name missing **")
            elif args == 3:
                print("** value missing **")


if __name__ == "__main__":
    """
    Entry point for the command-line interpreter.
    Initializes and starts the command loop.
    """
    HBNBCommand().cmdloop()
    readline.write_history_file(HISTORY_FILE)
