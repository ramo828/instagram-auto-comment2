@echo off

rmdir /s /q stp build dist
python -m venv stp
call stp\Scripts\activate.bat
pip install -r requirements.txt
pip install pip --upgrade
pyinstaller --onefile main.py --icon resource/icon.ico --noconsole
xcopy /s /e themes\ resource\ dist\