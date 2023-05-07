from PySide6 import QtWidgets, QtCore


class TableWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create table and set headers
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Age", "Gender"])

        # Add data to table
        data = [("Alice", 25, "Female"), ("Bob", 30, "Male"), ("Charlie", 35, "Male")]
        self.table.setRowCount(len(data))
        for i, (name, age, gender) in enumerate(data):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(age)))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(gender))

        # Set layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    table_widget = TableWidget()
    table_widget.show()
    app.exec_()
