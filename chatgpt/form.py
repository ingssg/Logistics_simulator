from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QSizePolicy, QVBoxLayout, QWidget


class EditableLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a layout for the widget
        layout = QVBoxLayout(self)

        # Create a line edit widget for editing the label text
        self.edit = QLineEdit(self)
        self.edit.setPlaceholderText("Enter label text and press Enter")
        self.edit.returnPressed.connect(self.update_label_text)
        layout.addWidget(self.edit)

        # Create a label widget for displaying the label text
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # Set the widget's size policy to expand vertically
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

    def update_label_text(self):
        # Get the text from the line edit widget and set it on the label widget
        text = self.edit.text()
        self.label.setText(text)

        # Hide the line edit widget and show the label widget
        self.edit.hide()
        self.label.show()

    def mousePressEvent(self, event):
        # Show the line edit widget and hide the label widget
        self.label.hide()
        self.edit.show()
        self.edit.setFocus()


if __name__ == "__main__":
    app = QApplication([])

    # Create an editable label widget and show it
    label_widget = EditableLabel()
    label_widget.show()

    app.exec_()
