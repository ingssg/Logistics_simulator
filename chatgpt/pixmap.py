from PySide6 import QtWidgets, QtGui, QtCore


class GraphicsPixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self):
        super().__init__()

        # Load two pixmaps
        pixmap1 = QtGui.QPixmap("image/u_arrow.png")
        pixmap2 = QtGui.QPixmap("image/d_l_arrow.png")

        # Combine the two pixmaps into a single pixmap
        combined_pixmap = QtGui.QPixmap(pixmap1.size())
        combined_pixmap.fill(QtGui.QColor(0, 0, 0, 0))
        painter = QtGui.QPainter(combined_pixmap)
        painter.drawPixmap(0, 0, pixmap1)
        painter.drawPixmap(0, 0, pixmap2)
        painter.end()

        # Set the combined pixmap to the QGraphicsPixmapItem
        self.setPixmap(combined_pixmap)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    scene = QtWidgets.QGraphicsScene()
    item = GraphicsPixmapItem()
    scene.addItem(item)
    view = QtWidgets.QGraphicsView(scene)
    view.show()
    app.exec_()
