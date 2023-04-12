rm stp build dist -rf
python -m venv stp
source stp/bin/activate
pip install -r requirements.txt
pip install pip --upgrade
pyinstaller --onefile main.py --icon icon.ico --noconsole
cp themes/ resorues/ dist -rf
