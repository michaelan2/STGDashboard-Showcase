@ECHO ON
CD /d %~dp0
CMD /c ipconfig
CMD /k "venv\scripts\activate & python __init__.py --host=0.0.0.0"