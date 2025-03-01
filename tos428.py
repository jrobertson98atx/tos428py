#! /usr/bin/python3

import argparse
import serial
import pathlib
import re

######################################################################

class tos428(object):

    # Commands not yet implemented
    # getpurpose,%i
    # setpurpose,%i,%s
    # getscope,%i
    # setscope,%i,%i,%i,%i,%i
    # getkeycodes,%i,%s
    # setkeycodes,%i,%s,%s,%s,%s
    # dumpeeprom
    # getversion
    # getmcu

    @classmethod
    def __get_428_device(cls):
        """
        Returns the name of the /dev/tty device corresponding to the tos 428 controller.

        Returns:
           str - The string name of the tos 428 device
        """
        retval = None
        uevent_files = pathlib.Path("/sys/class/tty/").glob("tty*/device/uevent")
        for file in uevent_files:
            with open(file, "r") as fp:
                file_contents = fp.read()

                product_string = "^PRODUCT=2341/8036/100$"
                match = re.search(product_string, file_contents, flags=re.MULTILINE)
                if match is not None:
                    # file.parts is:
                    # ('/', 'sys', 'class', 'tty', 'ttyACM0', 'device', 'uevent')
                    devname = file.parts[4]
                    retval = f"/dev/{devname}"
                    break

        assert retval != None, "ERROR: Could not find TOS device"
        return retval

    def __send_command(self, str_command : str):
        if self.debug: print(f"DBG: device={self.device}")
        if self.debug: print(f"DBG: command={str_command}")
        byte_command = str_command.encode()

        # Open the TOS GRS port provided - e.g. /dev/ttyACM0.  add a timeout
        # incase there are any issues (so it doesn't hang).  < 1 second doesn't
        # allow enough time to get an "ok" if controller has to change joystick
        # directions, allowing time for servos to respond
        tty = serial.Serial(self.device, baudrate=115200, timeout=1, write_timeout=1)
        tty.write(byte_command)

        # Read the response as a string, stripping newline characters
        response = tty.readline()
        tty.close()

        retval = response.decode().rstrip()

        if self.debug: print(f"DBG: retval={retval}")
        return retval

    def __init__(self):
        """
        Create a new class to interface with the TOS 428 controller
        """
        self.device = tos428.__get_428_device()
        self.debug = False
        pass

    def initialize(self, debug : bool):
        self.debug = debug
        pass

    def getwelcome(self):
        """
        Returns:
           str - string with the product name and firmware version
        """
        command = "getwelcome"
        retval = self.__send_command(command)
        return retval

    def getkeylist(self):
        """
        getkeylist provides a list of supported symbolic key names to the remote
        system. Those key names are useful as buttons can be
        configured to act as a USBkeyboard key and send emulated keystrokes for up
        to 3 simultaneously pressed keys
        (e.g. combination KEY_LEFT_CTRL,KEY_LEFT_ALT,KEY_DELETE would be possible.)

        Returns:
           str - current keylist for the controller
        """
        command = "getkeylist"
        retval = self.__send_command(command)
        return retval

    def getway(self, portnum : int):
        """
        Get the way (4 vs. 8) for the given port number

        Args:
            portnum (int) : Which port to get the way for

        Returns:
            str - The way for the given port (4 or 8)
        """
        command = f"getway,{portnum}"
        retval = self.__send_command(command)
        return retval

    def setway(self, way : int):
        """
        Set the way (4 vs. 8) for all ports on the controller

        Args:
            way (int) : Way to set (4 or 8)

        Returns:
            str - "ok" on success; "err" on failure
        """
        command = f"setway,all,{way}"
        retval = self.__send_command(command)
        return retval

    def getstartupway(self):
        """
        Get the startupway for the controller board

        Returns:
            str - The integer way number on success; "err" on failure
        """
        command = "getstartupway"
        retval = self.__send_command(command)
        return retval

    def setstartupway(self, way : int):
        """
        Set the startupway (4 vs. 8) for the controller

        Args:
            way (int) : Way to set (4 or 8)

        Returns:
            str - "ok" on success; "err" on failure
        """
        command = f"setstartupway,{way}"
        retval = self.__send_command(command)
        return retval

    def getangle(self, portnum, way):
        """
        Get the current angle for the given port and way

        Args:
            portnum (int) : Which port to get the angle for
            way (int) : Way (4 or 8) to get the angle for

        Returns:
            str - The current angle on success; "err" on failure
        """
        command = f"getangle,{portnum},{way}"
        retval = self.__send_command(command)
        return retval

    def setangle(self, way, angle):
        """
        Set the current angle for the given way

        Args:
            way (int) : Way (4 or 8) to set the angle for

        Returns:
            str - "ok" on success; "err" on failure
        """
        command = f"setangle,all,{way},{angle}"
        retval = self.__send_command(command)
        return retval

    def getcolor(self, way):
        """
        Get the current RGB color for the given way

        Args:
            way (int) : Way (4 or 8) to get the RGB color for

        Returns:
            str - The RGB color (e.g. 0,255,255) on success; "err" on failure
        """
        command = f"getcolor,{way}"
        retval = self.__send_command(command)
        return retval

    def setcolor(self, way : int, red : int, green : int, blue : int):
        """
        Set the current RGB color for the given way

        Args:
            way (int) : Way (4 or 8) to get the RGB color for
            red (int) : The red component of the color, 0-255
            green (int) : The green component of the color, 0-255
            blue (int) : The blue component of the color, 0-255

        Returns:
            str - The RGB color (e.g. 0,255,255) on success; "err" on failure
        """
        command = f"setcolor,{way},{red},{green},{blue}"
        retval = self.__send_command(command)
        return retval

    def sendcommand(self, command : str):
        """
        Send an arbitrary command string to the TOS428 board.

        Args:
           command (str): String sent verbatim to the TOS428 controller

        Returns:
           str - The string response from the controller
        """
        retval = self.__send_command(command)
        return retval

    def setuprom(self, romname : str):
        """
        Set the way (4 vs. 8) given the rom name

        Args:
            romname (str): The name of the rome file, which may include the full path

        Returns:
            str - "ok" on success; "err" on failure
        """
        numways = 8
        script_dir = pathlib.Path(__file__).resolve().parent
        romfile = pathlib.Path(script_dir.as_posix(), "roms4way.txt")
        with open(romfile, "r") as fp:
            file_contents = fp.read()
            romfile = pathlib.Path(romname).name
            matchstr = f"^{romfile}$"
            match = re.search(matchstr, file_contents, flags=re.MULTILINE)
            if match is not None:
                numways = 4

        if self.debug: print(f"DBG: setting ways to {numways} for '{romfile}'")
        retval = self.setway(numways)
        return retval

    def restorefactory(self):
        """
        Resets all settings to the factory default.

        Returns:
            str - "ok" on success; "err" on failure
        """
        command = "restorefactory"
        retval = self.__send_command(command)
        return retval

    def makepermanent(self):
        """
        Makes permanent (i.e. commits) any dynamic changes. This
        includes any calls to set* and restorefactory.

        Returns:
            str - "ok" on success; "err" on failure
        """
        command = "makepermanent"
        retval = self.__send_command(command)
        return retval

######################################################################

if __name__ == "__main__":

    usage = '''
    %(prog)s [-d|--debug] <subcommand> ....
    %(prog)s -h
    '''
    parser = argparse.ArgumentParser(description="Send a command to the 428 controller", usage=usage)
    parser.add_argument("-d", "--debug", action='store_true')
    subparsers = parser.add_subparsers(help="subcommand", dest="subcommand", required=True)

    device = tos428()

    port_choices = (1, 2, 3, 4)
    way_choices = (4, 8)

    help = "Get the welcome message from the device"
    child_parser = subparsers.add_parser("getwelcome", help=help)
    child_parser.set_defaults(func=lambda args: device.getwelcome())

    ## child_parser = subparsers.add_parser("getkeylist")
    ## child_parser.set_defaults(func=lambda args: device.getkeylist())

    help = "Get the current way (4 vs. 8) for the device"
    child_parser = subparsers.add_parser("getway", help=help)
    child_parser.add_argument("--portnum", "-p", default=1, choices=port_choices, type=int) 
    child_parser.set_defaults(func=lambda args: device.getway(args.portnum))
    
    help = "Set the way (4 vs. 8) for the device"
    child_parser = subparsers.add_parser("setway", help=help)
    child_parser.add_argument("way", choices=way_choices, type=int)
    child_parser.set_defaults(func=lambda args: device.setway(args.way))

    help = "Get the startup (i.e. power on) way for the device"
    child_parser = subparsers.add_parser("getstartupway", help=help)
    child_parser.set_defaults(func=lambda args: device.getstartupway())

    help = "Set the startup way for the device"
    child_parser = subparsers.add_parser("setstartupway", help=help)
    child_parser.add_argument("way", choices=way_choices, type=int)
    child_parser.set_defaults(func=lambda args: device.setstartupway(args.way))

    help = "Get the angle for the given way (4 vs. 8)"
    child_parser = subparsers.add_parser("getangle", help=help)
    child_parser.add_argument("--portnum", "-p", default=1, choices=port_choices, type=int) 
    child_parser.add_argument("way", choices=way_choices, type=int)
    child_parser.set_defaults(func=lambda args: device.getangle(args.portnum, args.way))
    
    help = "Set the angle for the given way (4 vs. 8)"
    child_parser = subparsers.add_parser("setangle", help=help)
    child_parser.add_argument("way", choices=way_choices, type=int)
    child_parser.add_argument("angle", type=int) 
    child_parser.set_defaults(func=lambda args: device.setangle(args.way, args.angle))
    
    help = "Get the RGB color for the given way (4 vs. 8)"
    child_parser = subparsers.add_parser("getcolor", help=help)
    child_parser.add_argument("way", choices=way_choices, type=int)
    child_parser.set_defaults(func=lambda args: device.getcolor(args.way))
    
    help = "Set the RGB color for the given way (4 vs. 8)"
    child_parser = subparsers.add_parser("setcolor", help=help)
    child_parser.add_argument("way", choices=way_choices, type=int)
    child_parser.add_argument("red", type=int)
    child_parser.add_argument("green", type=int)
    child_parser.add_argument("blue", type=int)
    child_parser.set_defaults(func=lambda args: device.setcolor(args.way, args.red, args.green, args.blue))

    help = "Set the way (4 vs. 8) for the given ROM name"
    child_parser = subparsers.add_parser("setuprom", help=help)
    child_parser.add_argument("romname", type=str)
    child_parser.set_defaults(func=lambda args: device.setuprom(args.romname))

    help = "Send an arbitrary command to the device"
    child_parser = subparsers.add_parser("sendcommand", help=help)
    child_parser.add_argument("command", type=str)
    child_parser.set_defaults(func=lambda args: device.sendcommand(args.command))

    help = "Restore all set* values to the factory defaults"
    child_parser = subparsers.add_parser("restorefactory", help=help)
    child_parser.set_defaults(func=lambda args: device.restorefactory())

    help = "Make any set* or restorefactory calls permanent"
    child_parser = subparsers.add_parser("makepermanent", help=help)
    child_parser.set_defaults(func=lambda args: device.makepermanent())

    args = parser.parse_args()
    device.initialize(args.debug)
    retval = args.func(args)
    print(f"{retval}")

