from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QDialog, QWidget, QLabel, QVBoxLayout
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6.QtGui import QTextCursor
from ui.loginUi import Ui_MainWindow
from ui.mainWindow import Ui_home as mainWindow
from ui.settings import Ui_Dialog as uis
from controls.app_controls import Setting_controls as sc
from controls.database import Database
from controls.backend_control import Worker
import threading as td
import sys


class Pencere(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.default_login = ''
        self.default_pass = ''
        self.style1 = [
            "themes/default.qss",
            "themes/besiktas.qss",
            "themes/galatasaray.qss",
            "themes/fenerbahce.qss",
            "themes/trabzonspor.qss",
            "themes/black.qss",
            "themes/light_blue.qss",
            "themes/yellow.qss",
            "themes/red.qss",
            "themes/purple.qss"]
        self.set = sc()
        self.db = Database()
        self.setupUi(self)
        self.logIn.clicked.connect(self.control)
        self.password.returnPressed.connect(self.control)
        self.passShow.clicked.connect(self.passEcho)
        theme = self.loadTheme()
        self.setStyleSheet(theme)
        self.work = Worker()
        self.flag = True


    def passEcho(self):
        ctrl = self.passShow.isChecked()
        if(ctrl):
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:    
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
        

    def control(self):
        _login = self.login.text()
        _password = self.password.text()
        if(_login == self.db.load_data(0) and _password == self.db.load_data(1)):
           self.mainUI()
        else:
            self.status.setText("Kullanıcı adı ve ya şifre yanlış")

    def mainUI(self):
        self.yeniPencere = mainWindow()
        theme = self.loadTheme()
        self.yeniPencere.setupUi(self, theme)
        self.yeniPencere.settings.triggered.connect(self.settUI)
        self.yeniPencere.exit.triggered.connect(self.quit)
        self.yeniPencere.about.triggered.connect(self.about)
        self.yeniPencere.c_load.clicked.connect(self.command_load)
        self.yeniPencere.c_save.clicked.connect(self.command_save)
        self.yeniPencere.spamController.clicked.connect(self.spamControl)
        self.yeniPencere.quit.clicked.connect(self.quit)
        self.yeniPencere.start.clicked.connect(self.startApp)
        self.yeniPencere.char_num.setDisabled(True)
        self.yeniPencere.spamOptions.setDisabled(True)
        self.work.log.connect(self.terminal_controller)
        self.work.success_counter_signal.connect(self.yeniPencere.comment_counter.setValue)
        self.work.try_counter_signal.connect(self.yeniPencere.try_count.setValue)
        self.yeniPencere.try_count.setDisabled(True)
        self.yeniPencere.comment_counter.setDisabled(True)


    def terminal_controller(self,data):
        cursor1 = QTextCursor(self.yeniPencere.terminal.textCursor())
        cursor1.movePosition(cursor1.MoveOperation.Down)
        self.yeniPencere.terminal.setTextCursor(cursor1)
        self.yeniPencere.terminal.insertPlainText(data)     

    def command_load(self):
        self.yeniPencere.comment.setPlainText(self.db.load_data(4))

    def command_save(self):
        comment = self.yeniPencere.comment.toPlainText()
        self.db.update_settings_column('comment', comment)

    def settUI(self):
        dialog = QDialog(self)
        theme = self.loadTheme()
        self.settingUI = uis()
        self.settingUI.setupUi(dialog, theme)
        self.settingUI.pshow.clicked.connect(self.showPassword)
        self.settingUI.pshow1.clicked.connect(self.showPassword)
        self.settingUI.pass_try.textChanged.connect(self.controlPassword)
        self.settingUI.save_quit.clicked.connect(self.save_and_quit)
        self.settingUI.theme.currentIndexChanged.connect(self.getTheme)
        self.settingUI.user.setText(self.db.load_data(0))
        self.settingUI.iuser.setText(self.db.load_data(2))
        self.settingUI.ipass.setText(self.db.load_data(3))
        dialog.exec()

    def loadTheme(self):
        theme = ''
        index = self.db.load_data(5)
        with open(self.style1[index]) as qss:
            theme = qss.read()
        return theme

    def getTheme(self):
        index = self.settingUI.theme.currentIndex()
        with open(self.style1[index]) as qss:
            self.setStyleSheet(qss.read())
            print(qss.read())
            print(self.style1[index])
        
           
    def spamControl(self):
        spamStatus = self.yeniPencere.spamController.isChecked()
        if(spamStatus):
            self.yeniPencere.char_num.setEnabled(True)
            self.yeniPencere.spamOptions.setEnabled(True)

        else:
            self.yeniPencere.char_num.setDisabled(True)
            self.yeniPencere.spamOptions.setDisabled(True)

    def about(self):
        h = 300
        w = 120
        theme = self.loadTheme()
        dialog = QDialog(self)
        dialog.setWindowTitle("Hakkında")
        dialog.setModal(True)
        dialog.resize(h, w)
        dialog.setStyleSheet(theme)
        # Label oluşturun
        label = QLabel("""
        Bu program özel olarak RamoSoft'a yapılmışdır ve tüm hakları saklıdır.
            iletisim Bilgileri
        email: illegalism666@gmail.com
        whatsapp: +994558302766
        """, dialog)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: red;")
        label.move(int(h/2), int(w/2))
        # Düzen oluşturun ve label'i ekleyin
        layout = QVBoxLayout(dialog)
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec()

    def showPassword(self):
        ps = self.settingUI.pshow.isChecked()
        ps1 = self.settingUI.pshow1.isChecked()
        if(ps):
            self.settingUI.pass1.setEchoMode(QLineEdit.EchoMode.Normal)
            self.settingUI.pass2.setEchoMode(QLineEdit.EchoMode.Normal)
            self.settingUI.pass_try.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.settingUI.pass1.setEchoMode(QLineEdit.EchoMode.Password)
            self.settingUI.pass2.setEchoMode(QLineEdit.EchoMode.Password)
            self.settingUI.pass_try.setEchoMode(QLineEdit.EchoMode.Password)
        if(ps1):
            self.settingUI.ipass.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.settingUI.ipass.setEchoMode(QLineEdit.EchoMode.Password)

    def controlPassword(self):
        ps1 = self.settingUI.pass2.text()
        ps2 = self.settingUI.pass_try.text()
        if(ps1 == ps2):
            self.settingUI.pass2.setStyleSheet('color: black;')
            self.settingUI.pass_try.setStyleSheet('color: black;')
        else:
            self.settingUI.pass_try.setStyleSheet('color: red;')
            self.settingUI.pass2.setStyleSheet('color: red;')

    def save_and_quit(self):
        password = ""
        old_password = self.db.load_data(1)
        # kohne sifreni vb'dan al
        ps = self.settingUI.pass1.text()
        ps1 = self.settingUI.pass2.text()
        ps2 = self.settingUI.pass_try.text()
        if(not ps1):
            ps = old_password
        # eger hec bir sey daxil edilmeyibse sifreleri eynilesdir ve seti yerine yetir

        if(old_password == ps):
        # eger kohne sifre uygundursa sertleri yerine yetir
            self.settingUI.pass1.setStyleSheet('color: black;')
        # sifre dogrudursa input rengini qoru
            if(ps1 == ps2):
        # sifre tekrari eynidirse serti yerine yetir
                password = ps1
                ips1 = self.settingUI.ipass.text()
                index = self.settingUI.theme.currentIndex()
                self.db.save_data_index(5,index)
                luser = self.settingUI.iuser.text()
                user = self.settingUI.user.text()
                self.set.checkSettingData(
                                        user, 
                                        password,
                                        luser,
                                        ips1
                                        )
                exit()

            else:
                password = ''
        else:
            self.settingUI.pass1.setStyleSheet('color: red;')
            # sifre kohne sifre ile uygun deyilse input'u qirmizi renge boya
            print(ps, old_password)


        
    def quit(self):
        exit()

    def startApp(self):
        spControl = self.yeniPencere.spamController.isChecked()
        page = self.yeniPencere.ipage.text()
        san = int(self.yeniPencere.d_time.text())
        comment = str(self.yeniPencere.comment.toPlainText())

        if(not spControl):
            char_num = 0
        else:
            char_num = int(self.yeniPencere.char_num.text())
            # print(char_num)
        print(char_num)
        spam_options = self.yeniPencere.spamOptions.currentIndex()
        self.work.setData(san, page,char_num, spam_options, comment)

        if self.flag == True:
            self.yeniPencere.start.setText("Durdur")
            self.flag = False
        else:
            self.yeniPencere.start.setText("Başla")
            self.flag = True
        self.thread = td.Thread(target=self.work.runBot, daemon=True) # type: ignore

        if(self.flag):
            print("Durdu")
            # self.thread.start()
            self.work.stopBot(False)
        else:
            print("Calisdi")
            self.yeniPencere.terminal.clear()
            self.work.stopBot(True)
            self.thread.start()

app = QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec())