from PyQt6.QtWidgets import QApplication, QMainWindow

from MoneyTracker.MONEY_TRACK.ui.WindowEarningExt import WindowEarningExt

app=QApplication([])
mainwindow=QMainWindow()
myui=WindowEarningExt()
myui.setupUi(mainwindow)
myui.showWindow()
app.exec()