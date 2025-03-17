import json
import os
import traceback
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from MoneyTracker.MONEY_TRACK.models.MTuser import MTuser
from MoneyTracker.MONEY_TRACK.ui.WindowRegister import Ui_MainWindow

class WindowRegisterExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()
        self.lineEditName.setFocus()

    def setupSignalAndSlot(self):
        self.pushButtonBack.clicked.connect(self.process_back)
        self.pushButtonEnter.clicked.connect(self.process_enter)

    def process_back(self):
        """Quay lại màn hình đăng nhập"""
        from MoneyTracker.MONEY_TRACK.ui.WindowLoginExt import WindowLoginExt  # Import muộn
        self.MainWindow.close()
        self.window_login = QMainWindow()
        self.login_ui = WindowLoginExt()
        self.login_ui.setupUi(self.window_login)
        self.window_login.show()

    def process_enter(self):
        """Xử lý đăng ký tài khoản"""
        dataset_path = "../dataset/mtusers.json"
        name=self.lineEditName.text().strip()
        username = self.lineEditUserName.text().strip()
        password = self.lineEditPassword.text().strip()
        re_password = self.lineEditReenterPassword.text().strip()

        if not name or not username or not password or not re_password:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        if password != re_password:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Mật khẩu nhập lại không khớp!")
            return

        try:
            # Kiểm tra sự tồn tại của tệp trước khi đọc
            if os.path.exists(dataset_path):
                with open(dataset_path, "r", encoding="utf-8") as file:
                    users = json.load(file)
                    # Nếu dữ liệu không phải danh sách, khởi tạo danh sách rỗng
                    if not isinstance(users, list):
                        users = []
            else:
                users = []  # Nếu tệp không tồn tại, khởi tạo danh sách mới
        except (FileNotFoundError, json.JSONDecodeError):
            users = []  # Khởi tạo danh sách mới nếu có lỗi khi đọc tệp

        # Kiểm tra tên người dùng đã tồn tại hay chưa
        if any(user.get("Username") == username for user in users):
            QMessageBox.warning(self.MainWindow, "Lỗi", "Tài khoản đã tồn tại!")
            return

        # Thêm người dùng mới vào danh sách
        new_user = MTuser(name, username, password).to_dict()
        users.append(new_user)

        try:
            with open(dataset_path, "w", encoding="utf-8") as file:
                json.dump(users, file, indent=4, ensure_ascii=False)
        except Exception as e:
            traceback.print_exc()
            QMessageBox.warning(self.MainWindow, "Lỗi", f"Không thể ghi vào file dữ liệu: {e}")
            return

        QMessageBox.information(self.MainWindow, "Thành công", "Đăng ký thành công!")

        # Quay lại màn hình đăng nhập
        self.process_back()