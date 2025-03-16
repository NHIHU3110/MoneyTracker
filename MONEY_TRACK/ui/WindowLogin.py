# Form implementation generated from reading ui file '/Users/huynhthaonhi/PycharmProjects/MoneyTracker/MONEY_TRACK/ui/WindowLogin.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(839, 545)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../images/image-Photoroom.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-10, 0, 851, 511))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../images/Login.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 230, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEditUserName = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEditUserName.setGeometry(QtCore.QRect(210, 220, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.lineEditUserName.setFont(font)
        self.lineEditUserName.setStyleSheet("QLineEdit {\n"
"    background-color: #f0f0f0; /* Nền mặc định */\n"
"    border: 2px solid #0066cc; /* Viền */\n"
"    border-radius: 10px; /* Bo góc */\n"
"    padding: 5px; /* Khoảng cách bên trong */\n"
"    color: #333; /* Màu chữ */\n"
"    font-size: 16px; /* Kích thước chữ */\n"
"    transition: background 0.3s ease; /* Thêm hiệu ứng chuyển màu nền */\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    background-color: #ffeb3b; /* Màu vàng nền khi hover */\n"
"    border-color: #ffcc00; /* Màu viền khi hover */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    background-color: #ffeb3b; /* Màu vàng nền khi focus */\n"
"    border-color: #ffcc00; /* Màu viền khi focus */\n"
"}\n"
"")
        self.lineEditUserName.setObjectName("lineEditUserName")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(100, 290, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEditPassword = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEditPassword.setGeometry(QtCore.QRect(210, 280, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.lineEditPassword.setFont(font)
        self.lineEditPassword.setStyleSheet("QLineEdit {\n"
"    background-color: #f0f0f0; /* Nền mặc định */\n"
"    border: 2px solid #0066cc; /* Viền */\n"
"    border-radius: 10px; /* Bo góc */\n"
"    padding: 5px; /* Khoảng cách bên trong */\n"
"    color: #333; /* Màu chữ */\n"
"    font-size: 16px; /* Kích thước chữ */\n"
"    transition: background 0.3s ease; /* Thêm hiệu ứng chuyển màu nền */\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    background-color: #ffeb3b; /* Màu vàng nền khi hover */\n"
"    border-color: #ffcc00; /* Màu viền khi hover */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    background-color: #ffeb3b; /* Màu vàng nền khi focus */\n"
"    border-color: #ffcc00; /* Màu viền khi focus */\n"
"}\n"
"")
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.pushButtonLogin = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonLogin.setGeometry(QtCore.QRect(112, 340, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonLogin.setFont(font)
        self.pushButtonLogin.setStyleSheet("/* Tùy chỉnh cho QTabWidget */\n"
"QTabWidget::pane {\n"
"    border: none; /* Xóa viền của QTabWidget */\n"
"    background-color: transparent; /* Nền trong suốt */\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4e79b0, stop:1 #1e5fa1); /* Gradient nền của tab */\n"
"    color: white; /* Màu chữ */\n"
"    border: 2px solid #1e5fa1; /* Viền tab */\n"
"    border-radius: 12px; /* Bo tròn góc của tab */\n"
"    padding: 12px; /* Khoảng cách giữa văn bản và viền */\n"
"    margin-right: 6px; /* Khoảng cách giữa các tab */\n"
"    font-size: 14px; /* Kích thước font chữ */\n"
"    font-weight: bold; /* Làm cho chữ đậm */\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1abc9c, stop:1 #16a085); /* Gradient nền của tab khi chọn */\n"
"    border-color: #1abc9c; /* Viền của tab khi chọn */\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #16a085, stop:1 #1abc9c); /* Gradient nền của tab khi hover */\n"
"}\n"
"\n"
"/* Tùy chỉnh cho các nút */\n"
"QPushButton {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9); /* Gradient nền của nút */\n"
"    color: white; /* Màu chữ */\n"
"    border: 2px solid #2980b9; /* Viền của nút */\n"
"    border-radius: 15px; /* Bo tròn góc của nút */\n"
"    padding: 15px 30px; /* Khoảng cách giữa văn bản và viền */\n"
"    font-size: 16px; /* Kích thước font chữ */\n"
"    font-weight: bold; /* Làm cho chữ đậm */\n"
"    transition: background-color 0.3s, border-color 0.3s, color 0.3s; /* Hiệu ứng chuyển màu */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1abc9c, stop:1 #16a085); /* Gradient nền của nút khi hover */\n"
"    color: white; /* Màu chữ khi hover */\n"
"    border-color: #16a085; /* Viền của nút khi hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #16a085, stop:1 #1abc9c); /* Gradient nền của nút khi nhấn */\n"
"    border-color: #1abc9c; /* Viền của nút khi nhấn */\n"
"    color: white; /* Màu chữ khi nhấn */\n"
"    transform: scale(0.98); /* Tạo hiệu ứng co lại khi nhấn */\n"
"}\n"
"\n"
"/* Tùy chỉnh cho các tab khi không chọn */\n"
"QTabBar::tab:!selected {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34495e, stop:1 #2c3e50); /* Gradient nền cho tab chưa chọn */\n"
"    border-color: #2c3e50; /* Viền cho tab chưa chọn */\n"
"    color: #ecf0f1; /* Màu chữ cho tab chưa chọn */\n"
"}\n"
"\n"
"/* Đảm bảo rằng tab có hiệu ứng khi hover */\n"
"QTabBar::tab:hover:!selected {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1abc9c, stop:1 #16a085); /* Gradient nền khi hover vào tab chưa chọn */\n"
"    border-color: #16a085;\n"
"}\n"
"\n"
"")
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.pushButtonRegister = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonRegister.setGeometry(QtCore.QRect(280, 340, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonRegister.setFont(font)
        self.pushButtonRegister.setStyleSheet("/* Tùy chỉnh cho QTabWidget */\n"
"QTabWidget::pane {\n"
"    border: none; /* Xóa viền của QTabWidget */\n"
"    background-color: transparent; /* Nền trong suốt */\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4e79b0, stop:1 #1e5fa1); /* Gradient nền của tab */\n"
"    color: white; /* Màu chữ */\n"
"    border: 2px solid #1e5fa1; /* Viền tab */\n"
"    border-radius: 12px; /* Bo tròn góc của tab */\n"
"    padding: 12px; /* Khoảng cách giữa văn bản và viền */\n"
"    margin-right: 6px; /* Khoảng cách giữa các tab */\n"
"    font-size: 14px; /* Kích thước font chữ */\n"
"    font-weight: bold; /* Làm cho chữ đậm */\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1abc9c, stop:1 #16a085); /* Gradient nền của tab khi chọn */\n"
"    border-color: #1abc9c; /* Viền của tab khi chọn */\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #16a085, stop:1 #1abc9c); /* Gradient nền của tab khi hover */\n"
"}\n"
"\n"
"/* Tùy chỉnh cho các nút */\n"
"QPushButton {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9); /* Gradient nền của nút */\n"
"    color: white; /* Màu chữ */\n"
"    border: 2px solid #2980b9; /* Viền của nút */\n"
"    border-radius: 15px; /* Bo tròn góc của nút */\n"
"    padding: 15px 30px; /* Khoảng cách giữa văn bản và viền */\n"
"    font-size: 16px; /* Kích thước font chữ */\n"
"    font-weight: bold; /* Làm cho chữ đậm */\n"
"    transition: background-color 0.3s, border-color 0.3s, color 0.3s; /* Hiệu ứng chuyển màu */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1abc9c, stop:1 #16a085); /* Gradient nền của nút khi hover */\n"
"    color: white; /* Màu chữ khi hover */\n"
"    border-color: #16a085; /* Viền của nút khi hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #16a085, stop:1 #1abc9c); /* Gradient nền của nút khi nhấn */\n"
"    border-color: #1abc9c; /* Viền của nút khi nhấn */\n"
"    color: white; /* Màu chữ khi nhấn */\n"
"    transform: scale(0.98); /* Tạo hiệu ứng co lại khi nhấn */\n"
"}\n"
"\n"
"/* Tùy chỉnh cho các tab khi không chọn */\n"
"QTabBar::tab:!selected {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34495e, stop:1 #2c3e50); /* Gradient nền cho tab chưa chọn */\n"
"    border-color: #2c3e50; /* Viền cho tab chưa chọn */\n"
"    color: #ecf0f1; /* Màu chữ cho tab chưa chọn */\n"
"}\n"
"\n"
"/* Đảm bảo rằng tab có hiệu ứng khi hover */\n"
"QTabBar::tab:hover:!selected {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1abc9c, stop:1 #16a085); /* Gradient nền khi hover vào tab chưa chọn */\n"
"    border-color: #16a085;\n"
"}\n"
"")
        self.pushButtonRegister.setObjectName("pushButtonRegister")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 839, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Username:"))
        self.label_3.setText(_translate("MainWindow", "Password:"))
        self.pushButtonLogin.setText(_translate("MainWindow", "Login"))
        self.pushButtonRegister.setText(_translate("MainWindow", "Register"))
