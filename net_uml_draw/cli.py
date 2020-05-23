#!/usr/bin/env python3

__author__ = "j3p0uk"

import net_uml_draw
import sys


def main():
    status = 0
    # Check arguments
    #   * Sheet Name
    #   * Key Column IDs
    #   * Output file

    # Create diagram
    nud = net_uml_draw.NetUMLDraw()
    nud.read_data()
    nud.process_data()
    nud.write_plant_uml()

    # Exit with status
    sys.exit(status)
