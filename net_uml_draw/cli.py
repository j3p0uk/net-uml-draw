#!/usr/bin/env python3

__author__ = "j3p0uk"

from net_uml_draw import NetUMLDraw


def main():
    # Check arguments
    #   * Sheet Name
    #   * Key Column IDs
    #   * Output file

    # Create diagram
    nud = NetUMLDraw()
    nud.read_data()
    nud.process_data()
    nud.write_plant_uml()
