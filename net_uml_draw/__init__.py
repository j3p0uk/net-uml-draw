#!/usr/bin/env python3

__author__ = "j3p0uk"

import numpy as np
import textwrap
from . import sheets


class NetUMLDraw(object):
    """
    @startuml
    frame "Room 1" as 1 {
        frame "Switch 1" as 2 {
            queue "Port1" as 3
            queue "Port2" as 4
        }
        frame "Device 1" as 5 {
            queue "LAN" as 6
        }
        frame "Device 2" as 7 {
            queue "LAN" as 8
        }
    }
    frame "Room 2" as 9 {
        frame "Switch 2" as 10 {
            queue "Port1" as 11
            queue "Port2" as 12
        }
        frame "Device 3" as 13 {
            queue "LAN" as 14
        }
    }
    3 -- 6
    4 -- 8
    11 -- 14
    @enduml
    """
    start = '@startuml'
    end = '@enduml'

    def __init__(self):
        self.data = None
        self.obj = 0
        self.rooms = {}
        self.indent = '    '
        self.sheets = sheets.Sheets()

    def read_data(self):
        self.obj = 0
        self.rooms = {}
        self.data = self.sheets.get_values()

    def print_data(self):
        # Skipping the header line
        for line in self.data[1:]:
            print("{}".format(line))

    def process_data(self):
        # Get the row index alongside the data
        for obj, line in enumerate(self.data[1:], 2):
            # line[1]: Rooms - these are frames that contain frames
            # line[2]: Device - these are frames that contain queues as ports
            # line[3]: Port - these are queues to represent ports on a device
            # line[5]: Connections - these connect queues
            self.rooms.setdefault(line[1], {})
            if len(line) < 6:
                self.rooms[line[1]].setdefault(line[2], {})[line[3]] = (obj, None)
            else:
                # Split off just the number from the A1 notation returned
                conn = None
                try:
                    conn = int(line[5].lstrip("=A"))
                except ValueError:
                    print("Could not read int from '{}'.lstrip(\"=A\")".format(line[5]))
                self.rooms[line[1]].setdefault(line[2], {})[line[3]] = (obj, conn)

    def room_string(self, room):
        self.obj += 1
        return 'frame "{}" as {} {{'.format(room, self.obj)

    def device_string(self, device):
        self.obj += 1
        return textwrap.indent('frame "{}" as {} {{'.format(device, self.obj), self.indent)

    def port_string(self, conn):
        self.obj += 1
        return textwrap.indent('queue "{}" as {}'.format(conn, self.obj), self.indent + self.indent)

    def write_plant_uml(self):
        print(self.start)
        lookup = {}
        for room in self.rooms.keys():
            print(self.room_string(room))
            for device in self.rooms[room].keys():
                print(self.device_string(device))
                for conn in self.rooms[room][device].keys():
                    print(self.port_string(conn))
                    lookup[self.obj] = {}
                    this, that = self.rooms[room][device][conn]
                    lookup[self.obj]['this'] = this
                    lookup[self.obj]['that'] = that
                print(textwrap.indent('}', self.indent))
            print('}')
        conns = []
        for k, v in lookup.items():
            for key in lookup.keys():
                if lookup[key]['this'] == v['that']:
                    conns.append('{} -- {}'.format(min(k, key), max(k, key)))
                    break
        print('\n'.join(np.unique(conns)))
        print(self.end)
