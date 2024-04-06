from logger import Logger

from PySide2.QtGui import QFont, QIcon

def load_font_size():
    default_font_size = 10
    try:
        file = open("config/font_size.config", 'r')
    except FileNotFoundError:
        Logger.log_error("Config file of font size was not found. Default font size will be used.")
        return default_font_size
    font_size_str = file.read()
    try:
        font_size = int(font_size_str)
    except ValueError:
        Logger.log_error("Config file of font size should contain only a single integer. Default font size will be used.")
        return default_font_size
    if font_size < 4 or font_size > 30:
        Logger.log_error("Config file of font size contains font size out of range. Default font size will be used.")
        return default_font_size
    return font_size

class FontGlobal:
    font_size = load_font_size()
    font = QFont("Verdana", font_size)
    font_header = QFont("Verdana", int(font_size * 1.2))

def export_font_size():
    try:
        file = open("config/font_size.config", 'w')
    except PermissionError:
        Logger.log_error("You don't have permission to export font size to this config file.")
        return
    if FontGlobal.font_size is None:
        Logger.log_error("Cannot export None font size to config file.")
        return
    file.write(str(FontGlobal.font_size))
