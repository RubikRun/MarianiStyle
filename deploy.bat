pyinstaller --hidden-import PySide2 --add-data "icons/date_arrow_left.png;." main.py
xcopy icons dist\main\icons /E /I
xcopy data dist\main\data /E /I
