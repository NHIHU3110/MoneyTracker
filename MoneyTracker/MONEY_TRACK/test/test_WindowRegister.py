from PyQt6.QtWidgets import QApplication, QMainWindow

from MoneyTracker.MONEY_TRACK.ui.WindowRegisterExt import WindowRegisterExt

app=QApplication([])
mainwindow=QMainWindow()
myui=WindowRegisterExt()
myui.setupUi(mainwindow)
myui.showWindow()
app.exec()