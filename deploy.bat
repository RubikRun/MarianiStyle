pyinstaller --hidden-import PySide6 --add-data "icons/date_arrow_left.png;." mainwindow.py
xcopy icons dist\mainwindow\icons /E /I
