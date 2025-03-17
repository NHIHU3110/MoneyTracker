from PyQt6.QtWidgets import QApplication, QMainWindow
from MoneyTracker.MONEY_TRACK.ui.WindowLoginExt import WindowLoginExt

app=QApplication([])
mainwindow=QMainWindow()
myui=WindowLoginExt()
myui.setupUi(mainwindow)
myui.showWindow()
app.exec()