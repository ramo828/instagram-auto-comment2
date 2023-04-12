@echo off
rd /s /q build
rd /s /q dist
python -m venv stp
call stp\Scripts\activate.bat
pip install -r requirements.txt
pip install pip --upgrade
pyinstaller --onefile main.py --icon icon.ico --noconsole
xcopy themes dist /s /e /h /y