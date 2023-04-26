from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton, QLabel, QTabBar

app = QApplication([])


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the tab widget and add it to the layout
        self.tab_widget = QTabWidget(self)
        self.tab_widget.addTab(QLabel('Tab 1'), 'Tab 1')
        self.tab_widget.addTab(QLabel('Tab 2'), 'Tab 2')

        # Create a custom tab bar with a new tab button
        self.tab_bar = QTabBar()
        self.tab_bar.addTabButton = QPushButton('+')
        self.tab_bar.addTabButton.clicked.connect(self.add_tab)
        self.tab_widget.setTabBar(self.tab_bar)

        # Add the tab widget to the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.tab_widget)

    def add_tab(self):
        # Create a new label for the tab content
        new_label = QLabel(f'Tab {self.tab_widget.count() + 1}')

        # Add the new label to a new tab in the tab widget
        self.tab_widget.addTab(new_label, f'Tab {self.tab_widget.count() + 1}')
        self.tab_widget.setCurrentIndex(
            self.tab_widget.count() - 1)  # Set focus to new tab


# Create the main window
main_window = QMainWindow()

# Create the main widget and set it as the central widget of the main window
main_widget = MainWidget()
main_window.setCentralWidget(main_widget)

# Show the main window
main_window.show()

app.exec()
