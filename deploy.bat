pyinstaller --hidden-import PySide2 --add-data "icons/date_arrow_left.png;." main_window.py
xcopy icons dist\main_window\icons /E /I
xcopy database dist\main_window\database /E /I
