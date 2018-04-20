@echo off

rem set the python path
set pythonPath=G:\Programming\WinPython-64bit-3.6.3.0Qt5\python-3.6.3.amd64

echo [START] converting .ui files...

rem convert all .ui files in the current directory
for %%i in (*.ui) do (

   rem Display the file name
   echo %%i   --  ui_%%~ni.py

   rem converting
   %pythonPath%\python.exe -m PyQt5.uic.pyuic -x %%i -o ui_%%~ni.py


)

echo [END] converting .ui files...