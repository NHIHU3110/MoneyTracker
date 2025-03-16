import traceback
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from MONEY_TRACK.libs.DataConnector import DataConnector
from MONEY_TRACK.ui.MainWindowExt import MainWindowExt
from MONEY_TRACK.ui.WindowLogin import Ui_MainWindow

class WindowLoginExt(Ui_MainWindow):
   def setupUi(self, MainWindow):
       super().setupUi(MainWindow)
       self.MainWindow = MainWindow
       self.setupSignalAndSlot()

   def showWindow(self):
       self.MainWindow.show()

   def setupSignalAndSlot(self):
       self.pushButtonLogin.clicked.connect(self.process_login)
       self.pushButtonRegister.clicked.connect(self.process_register)

   def process_login(self):
       username = self.lineEditUserName.text().strip()
       password = self.lineEditPassword.text().strip()

       if not username or not password:
           QMessageBox.warning(self.MainWindow, "ERROR", "Please fill in your login information completely!")
           return

       try:
           dc = DataConnector()
           mtuser = dc.login(username, password)

           if mtuser is not None:
               QMessageBox.information(self.MainWindow, "Login Successful",
                                        "Login successful, welcome to Money Track!")
               self.MainWindow.close()
               self.mainwindow = QMainWindow()
               self.myui = MainWindowExt()
               self.myui.setupUi(self.mainwindow)
               self.myui.showWindow(username, password)
           else:
               QMessageBox.warning(self.MainWindow, "Login Failed",
                                   "Incorrect username or password. Please try again or create a new account!")
       except Exception as e:
           traceback.print_exc()
           QMessageBox.critical(self.MainWindow, "ERROR", f"Đã xảy ra lỗi trong quá trình đăng nhập: {str(e)}")

   def process_register(self):
       from MONEY_TRACK.ui.WindowRegisterExt import WindowRegisterExt  # Import muộn
       self.MainWindow.close()
       self.window_register = QMainWindow()
       self.register_ui = WindowRegisterExt()
       self.register_ui.setupUi(self.window_register)
       self.register_ui.showWindow()