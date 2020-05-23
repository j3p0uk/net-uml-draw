#!/usr/bin/env python

__author__ = "j3p0uk"

import net_uml_draw
import nose
import sys
import unittest.mock


class ExitException(Exception):
    pass


class TestNetUMLDrawCli(object):

    @unittest.mock.patch('net_uml_draw.NetUMLDraw', autospec=True)
    def test_uml_draw_cli(self, mock_nud):
        sys.argv = ['net-uml-draw']
        with unittest.mock.patch('sys.exit', side_effect=ExitException) as mock_exit:
            nose.tools.assert_raises(ExitException, net_uml_draw.cli.main)
            mock_exit.assert_called_with(0)
            calls = [unittest.mock.call().read_data(),
                     unittest.mock.call().process_data(),
                     unittest.mock.call().write_plant_uml()]
            print(mock_nud.method_calls)
            nose.tools.ok_(mock_nud.method_calls == calls)
