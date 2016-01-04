"""
csgo-autoaccept

Provides base functionality for all matchmaking services.
"""

import ctypes
import re

import win32api
import win32gui
from PIL import ImageGrab

def aero_enabled():
    """
    Check if Windows Aero is enabled.

    Returns:
        bool: Whether or not Windows Aero is enabled.
    """

    try:
        hasAero = ctypes.c_bool()
        retcode = ctypes.windll.dwmapi.DwmIsCompositionEnabled(ctypes.byref(hasAero))
        return retcode == 0 and hasAero.value
    except AttributeError:
        return False

def get_hwnd(window_title):
    """
    Get the HWND for any window it can find.

    Returns:
        int: HWND of window if it is found.
        bool: False if no window exists.
    """

    def _handle_hwnd(hwnds, hwnd, extra):
        if re.match(window_title, win32gui.GetWindowText(hwnd)):
            hwnds.append(hwnd)

    hwnds = []
    win32gui.EnumWindows(lambda hwnd, extra: _handle_hwnd(hwnds, hwnd, extra), None)
    return hwnds[0] if hwnds else False

def focused(window_title):
    """
    Check if the window is focused (in the foreground).

    Returns:
        bool: Whether or not the window is focused.
    """

    return win32gui.GetForegroundWindow() == get_hwnd(window_title)

def exists(window_title):
    """
    Check if it can find an open window.

    Returns:
        bool: Whether or not the window exists.
    """

    return get_hwnd(window_title) is not False

def screenshot(window_title):
    """
    Take a screenshot of the window if it exists.

    Returns:
        Image: Image data for the screenshot taken.
        bool: False if no window exists.
    """

    hwnd = get_hwnd(window_title)
    return ImageGrab.grab(win32gui.GetWindowRect(hwnd)) if hwnd else False
