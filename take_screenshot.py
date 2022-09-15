#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A simple tool for taking consistent screenshots of PySolFC

Requires wmctrl, xprop, and ImageMagic's import command to be installed.
"""

__author__ = "Stephan Sokolow (deitarion/SSokolow)"
__appname__ = "PySolFC Screenshot Helper"
__version__ = "0.0pre0"
__license__ = "MIT"

#: The window geometry to be screenshotted
WANT_GEOM = b"0,1300,20,1280,960"

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from time import sleep
from subprocess import Popen, check_call, check_output  # nosec


class WaitTimedOut(Exception):
    """Timed out in `wait_for_window`"""


def wait_for_window(wm_title: bytes, wm_class: bytes, timeout=10) -> bytes:
    """Wait for a specified window to exist and return its X11 window ID"""
    waited = 0
    while waited < timeout:
        for line in check_output([b'wmctrl', b'-l']).split(b'\n'):  # nosec
            # Skip lines of the wrong format
            fields = line.split(None, 3)
            if len(fields) != 4:
                continue

            # If we get a title match, use xprop to confirm the window class
            # (i.e. to make sure it's not a terminal pointing at a folder of
            # the same name)
            xid, _desktop, _host, title = fields
            if wm_title in title:
                cls = check_output([b'xprop', b'-id', xid,  # nosec
                    b'u', b'=$0', b'WM_CLASS'
                                    ]).split(b'=', 1)[-1].strip().strip(b'"')
                if cls == wm_class:
                    return xid
        sleep(1)
        waited += 1
    raise WaitTimedOut()


def take_screenshot(filename: bytes):
    """Start PySolFC, wait for the main window, position it to match
    `DESIRED_GEOM`, save a screenshot to ``filename``, and then kill it."""
    pysol = Popen(['python3', 'pysol.py'])  # nosec
    try:
        print("Waiting for PySolFC's main window...")
        xid = wait_for_window(b"PySol - ", b'pySol')

        print("Resizing window...")
        check_call([b"wmctrl", b"-i", b"-r", xid,
            b"-b" b"remove,maximized_vert,maximized_horz"])
        check_call([b"wmctrl", b"-i", b"-r", xid, b"-b" b"add,above"])
        check_call([b"wmctrl", b"-i", b"-r", xid, b"-e", WANT_GEOM])  # nosec

        # If it was maximized, it may actually need more than one second
        print("Giving PySol time to rescale...")
        sleep(2)

        print("Taking Screenshot...")
        check_call([b"import", b"-window", xid, filename])
    finally:
        print("Terminating PySolFC...")
        pysol.terminate()


def main():
    """The main entry point, compatible with setuptools entry points."""
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
        description=__doc__.replace('\r\n', '\n').split('\n--snip--\n')[0])
    parser.add_argument('--version', action='version',
        version="%%(prog)s v%s" % __version__)

    args = parser.parse_args()

    take_screenshot("test.png")


if __name__ == '__main__':  # pragma: nocover
    main()

# vim: set sw=4 sts=4 expandtab :
