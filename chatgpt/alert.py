from PySide6.QtWidgets import QApplication, QMessageBox

app = QApplication([])

# Show a confirmation dialog
confirmation = QMessageBox()
confirmation.setWindowTitle("Confirmation")
confirmation.setText("Do you want to proceed?")
confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
confirmation.setDefaultButton(QMessageBox.No)
result = confirmation.exec_()

if result == QMessageBox.Yes:
    print("User clicked Yes")
else:
    print("User clicked No")

app.exec_()
