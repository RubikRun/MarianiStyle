from logger import Logger
from database.data_io import DataIO

from PySide2.QtGui import QColor

def load_colors():
    default_colors = [QColor(255, 0, 0, 255), QColor(0, 255, 0, 255), QColor(0, 0, 255, 255), QColor(90, 140, 200, 200), QColor(140, 90, 180, 200)]
    try:
        file = open("config/colors.config", 'r', encoding = "utf-8")
    except FileNotFoundError:
        Logger.log_error("Config file of colors was not found. Default colors will be used.")
        return default_colors

    colors = []
    for line in file:
        if line.startswith('#'):
            continue
        color = DataIO.parse_color(line, ';')
        if color is not None:
            colors.append(color)

    if len(colors) < 3:
        Logger.log_error("Config file of colors must contain at least 3 colors. Default colors will be used.")
        return default_colors

    return colors

class ColorsGlobal:
    colors = load_colors()

def export_colors():
    try:
        file = open("config/colors.config", 'w', encoding = "utf-8")
    except PermissionError:
        Logger.log_error("You don't have permission to export colors to this config file.")
        return
    if ColorsGlobal.colors is None or len(ColorsGlobal.colors) == 0:
        Logger.log_error("Cannot export None or empty colors to config file.")
        return

    for color in ColorsGlobal.colors:
        parts = [color.red(), color.green(), color.blue(), color.alpha()]
        decl = DataIO.create_declaration(parts, "iiii", ';')
        file.write(decl + "\n")
