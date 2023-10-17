#!/usr/bin/python3
""" Holbie Chess Console """


import cmd
from models.base_model import BaseModel
from models.user import User
from models import storage


class HolbieChessCmd(cmd.Cmd):
    """
    Defines the HolbieChessCmd class
    """
    prompt = "HolbieChess $ "
    modules = {
        "BaseModel": BaseModel,
        "User": User
    }

    def do_quit(self, arg):
        """
        Exits the program.
        Usage: quit
        """
        return True

    def do_EOF(self, arg):
        """
        Allows clean exit with ^D
        """
        return True

    def emptyline(self):
        """
        Prevents the program from exiting if an emptyline is passed
        """
        pass

    def do_create(self, class_name):
        """
        Creates a new instance of the specified class and saves it to the
        JSON file. Prints the id of the new instance to indicate success.

        Usage: create <class_name>
        """
        if not class_name:
            print("** class name missing **")
            return

        if class_name not in HolbieChessCmd.modules:
            print("** class doesn't exist **")
            return

        obj = HolbieChessCmd.modules[class_name]()
        obj.save()
        print(obj.id)

    def do_all(self, class_name=None):
        """
        Prints all string representations of all instances. If a class name is
        indicated, prints only the instances of this class.

        Usage: all <?class_name>
        """
        if class_name:
            if class_name not in HolbieChessCmd.modules:
                print("** class doesn't exist**")
                return

            objects = storage.all(class_name)
        else:
            objects = storage.all()

        for obj in objects.values():
            print(str(obj))

    def check_args(argv):
        """
        Checks if the command line arguments are valid.

        Args:
            argv (list): Arguments of the command line
        """
        if not argv or argv[0] is None:
            print("** class name missing **")
            return

        if argv[0] not in HolbieChessCmd.modules:
            print("** class doesn't exist **")
            return

        if len(argv) < 2:
            print("** instance id missing **")
            return

        obj_class = argv[0]
        obj_id = argv[1]

        if f"{obj_class}.{obj_id}" not in storage.all(obj_class):
            print("** no instance found **")
            return

        return True
    
    def objectify(argv):
        """
        Returns the string representation of an object

        Args:
            argv (list): Command line arguments
        """
        obj_class = argv[0]
        obj_id = argv[1]
        return f"{obj_class}.{obj_id}"

    def do_show(self, args):
        """
        Prints the string representation of an instance.

        Usage: show <class_name> <obj_id>
        """
        argv = args.split()
        if HolbieChessCmd.check_args(argv):
            obj = HolbieChessCmd.objectify(argv)
            objects = storage.all(argv[0])
            print(objects[obj])

    def do_delete(self, args):
        """
        Deletes an instance and saves the changes in the json file

        Usage: delete <class_name> <obj_id>
        """
        argv = args.split()
        if HolbieChessCmd.check_args(argv):
            obj = HolbieChessCmd.objectify(argv)
            objects = storage.all(argv[0])
            del objects[obj]
            storage.save()

    def do_update(self, args):
        """
        Updates an instance by adding or updating an attribute. Saves the
        changes in the JSON file.
        
        Usage: update <class_name> <obj_id> <attribute_name> "<attribute_value>"
        """
        argv = args.split()

        if len(argv) < 3 or argv[2] is None:
            print("** attribute name missing **")
            return

        if len(argv) < 4 or argv[3] is None:
            print("** attribute value missing **")
            return

        obj = HolbieChessCmd.objectify(argv)
        objects = storage.all(argv[0])
        attr = argv[2]
        value = argv[3]

        setattr(objects[obj], attr, value)
        storage.save()
        

if __name__ == '__main__':
    HolbieChessCmd().cmdloop()
