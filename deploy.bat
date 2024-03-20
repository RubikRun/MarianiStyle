pyinstaller --hidden-import PySide2 --add-data "icons/date_arrow_left.png;." mainwindow.py
xcopy icons dist\mainwindow\icons /E /I
xcopy database dist\mainwindow\database /E /I
