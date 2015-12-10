"""
csgo-autoaccept

Provides specific functionality for Valve's official matchmaking service.
"""

import ctypes

import win32api
import win32gui
from PIL import ImageGrab

# use this to find csgo's hwnd
WINDOW_TITLE = "Counter-Strike: Global Offensive"
VALID_RGB = ((30, 113, 80))

def get_hwnd():
    """
    Get the HWND for any CS:GO window it can find.

    Returns:
        int: HWND of window if it is found.
        bool: False if no CS:GO window exists.
    """

    def _handle_hwnd(hwnds, hwnd, extra):
        if win32gui.GetWindowText(hwnd) == WINDOW_TITLE:
            hwnds.append(hwnd)

    hwnds = []
    win32gui.EnumWindows(lambda hwnd, extra: _handle_hwnd(hwnds, hwnd, extra), None)
    return hwnds[0] if hwnds else False

def focused():
    """
    Check if the CS:GO window is focused (in the foreground).

    Returns:
        bool: Whether or not the CS:GO window is focused.
    """

    return win32gui.GetForegroundWindow() == get_hwnd()

def exists():
    """
    Check if it can find an open CS:GO window.

    Returns:
        bool: Whether or not the CS:GO window exists.
    """

    return get_hwnd() is not False

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

def screenshot():
    """
    Take a screenshot of the CS:GO window if it exists.

    Returns:
        Image: Image data for the screenshot taken.
        bool: False if no CS:GO window exists.
    """

    hwnd = get_hwnd()
    return ImageGrab.grab(win32gui.GetWindowRect(hwnd)) if hwnd else False

def get_accept():
    """
    Find the accept button if the CS:GO window exists.

    Returns:
        tuple: x, y coordinates of accept button.
        bool: False if no CS:GO window exists or no accept button is found.
    """

    game = screenshot()
    if not game:
        return False
    elif not focused():
        return False

    startx, starty, _, _ = win32gui.GetWindowRect(get_hwnd())
    w, h = game.size
    pixels = game.load()
    # assume button is in top left quarter of game window
    for x in range(0, w // 2, 4): # skip 4 horizontal pixels at a time due to vertical gradient
        for y in range(0, h // 2):
            if pixels[x, y][:3] in VALID_RGB:
                return startx + x, starty + y
    return False
