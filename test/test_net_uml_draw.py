#!/usr/bin/env python

__author__ = "j3p0uk"

import io
import net_uml_draw
import nose.tools
import textwrap
import unittest

DATA = [
    ["Display Name and Port", "Room", "Device", "Port", "MAC", "Connected to", "Display Name"],
    ["", "Room 1", "Dev 1", "WiFi", "", "=A2", "Device 1"],
    ["", "Room 1", "Dev 1", "1", ""],
    ["", "Room 1", "Dev 1", "2", "", "=A5", ""],
    ["", "Room 2", "Dev 2", "LAN", "", "=A4", ""],
    ["", "Room 3", "Dev 3", "WiFi", "", "=A2", ""],
    ["", "Room 3", "Dev 4", "WiFi", "", "", "Display Name"]]


class TestNetUMLDraw(object):

    def __init__(self):
        self.nud = net_uml_draw.NetUMLDraw()
        self.nud.sheets = unittest.mock.MagicMock()

    def test_net_uml_draw(self):
        nose.tools.ok_(self.nud.data is None)
        nose.tools.ok_(self.nud.obj == 0)
        nose.tools.ok_(self.nud.rooms == {})
        nose.tools.ok_(self.nud.indent == '    ')

    def test_read_data(self):
        self.nud.data = [["header"], ["data"]]
        self.nud.obj = 10
        self.nud.rooms = {"room1": {}, "room2": {}}
        self.nud.sheets.get_values.return_value = [["header"], ["new_data"]]
        self.nud.read_data()
        nose.tools.ok_(self.nud.data == [["header"], ["new_data"]])
        nose.tools.ok_(self.nud.obj == 0)
        nose.tools.ok_(self.nud.rooms == {})

    def test_print_data(self):
        data = ["data"]
        self.nud.data = [["header"], data]
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.nud.print_data()
        printed_data = mock_stdout.getvalue().strip()
        print(printed_data)
        nose.tools.ok_(printed_data == data.__str__(), "Output {} doesn't match {}".format(
            printed_data, data))

    def test_process_data(self):
        self.nud.data = DATA
        self.nud.process_data()
        expected_dict = {'Room 1': {'Dev 1': {'WiFi': (2, 2), '1': (3, None), '2': (4, 5)}},
                         'Room 2': {'Dev 2': {'LAN': (5, 4)}},
                         'Room 3': {'Dev 3': {'WiFi': (6, 2)}, 'Dev 4': {'WiFi': (7, None)}}}
        nose.tools.ok_(self.nud.rooms == expected_dict, "Rooms '{}' doesn't match '{}'".format(
            self.nud.rooms, expected_dict))

    def test_room_string(self):
        self.nud.obj = 0
        ret_string = self.nud.room_string("Room 1")
        expected_string = 'frame "Room 1" as 1 {'
        nose.tools.ok_(ret_string == expected_string, "Return '{}' doesn't match '{}'".format(
            ret_string, expected_string))

    def test_device_string(self):
        self.nud.obj = 1
        ret_string = self.nud.device_string("Device 1")
        expected_string = textwrap.indent('frame "Device 1" as 2 {', self.nud.indent)
        nose.tools.ok_(ret_string == expected_string, "Return '{}' doesn't match '{}'".format(
            ret_string, expected_string))

    def test_port_string(self):
        self.nud.obj = 2
        ret_string = self.nud.port_string("Port 1")
        expected_string = textwrap.indent('queue "Port 1" as 3', self.nud.indent + self.nud.indent)
        nose.tools.ok_(ret_string == expected_string, "Return '{}' doesn't match '{}'".format(
            ret_string, expected_string))

    def test_write_plant_uml(self):
        self.nud.data = DATA
        self.nud.process_data()
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.nud.write_plant_uml()
        ret_string = mock_stdout.getvalue().strip()
        expected_string = '''
@startuml
frame "Room 1" as 1 {
    frame "Dev 1" as 2 {
        queue "WiFi" as 3
        queue "1" as 4
        queue "2" as 5
    }
}
frame "Room 2" as 6 {
    frame "Dev 2" as 7 {
        queue "LAN" as 8
    }
}
frame "Room 3" as 9 {
    frame "Dev 3" as 10 {
        queue "WiFi" as 11
    }
    frame "Dev 4" as 12 {
        queue "WiFi" as 13
    }
}
3 -- 11
3 -- 3
5 -- 8
@enduml'''.strip()
        nose.tools.ok_(ret_string == expected_string, "Return '{}' doesn't match '{}'".format(
            ret_string, expected_string))
