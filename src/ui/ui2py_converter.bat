@echo off

set pythonPath=G:\Programming\WinPython-64bit-3.6.3.0Qt5\python-3.6.3.amd64

for %%i in (*.ui) do (

   rem Выводим имя файла

   echo %%i

   %pythonPath%\python.exe -m PyQt5.uic.pyuic -x %%i -o ui_%%~ni.py
)
