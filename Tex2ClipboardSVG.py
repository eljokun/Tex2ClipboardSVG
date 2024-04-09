# TESTED IN PYTHON 3.12, CANNOT GUARANTEE COMPATIBILITY WITH OLDER VERSIONS
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLineEdit
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QMimeData, QByteArray, Qt
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QLabel
import tempfile
import sys
import io
import matplotlib.pyplot as plot


# Declare that we're using math text for matplotlib
plot.rc('mathtext', fontset='cm')
# Prepare byte I/O stream for image data to be transferred to clipboard
byteIO = io.BytesIO() # SVG
DPI = 300
FONT_SIZE = 12


def render(equation):
    # Get byte IO as global duh
    global byteIO
    # get global stuff
    global DPI
    global FONT_SIZE
    # matplotlib stuff lol
    try:
        img = plot.figure(figsize=(1, 1))
        img.text(0, 0, fr"${equation.rstrip()}$", FONT_SIZE=12, parse_math=True)
        img.savefig(byteIO, dpi=DPI, transparent=True, format='svg', bbox_inches='tight', pad_inches=0.1)
        plot.close(img)
    except:
        raise Exception('FAILED')


if __name__ == '__main__':
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.text_box = QLineEdit(self)
            self.text_box.setPlaceholderText("Input Equation [TeX]")
            self.text_box.textChanged.connect(self.renderticker)
            self.dpi_text_box = QLineEdit(self)
            self.dpi_text_box.setPlaceholderText("DPI - Default is 300 DPI")
            self.dpi_text_box.textChanged.connect(self.renderticker)
            self.fontsize_text_box = QLineEdit(self)
            self.fontsize_text_box.setPlaceholderText("Font Size [pt] - Default is 12")
            self.fontsize_text_box.textChanged.connect(self.renderticker)
            self.DPILabel = QLabel(f'Resolution: {DPI} DPI')
            self.fontsizelabel = QLabel(f'Font size: {FONT_SIZE} pt')
            self.setWindowTitle('Tex2ClipboardSVG')
            self.resize(800, 600)
            self.scene = QGraphicsScene(self)
            self.view = QGraphicsView(self.scene, self)
            layout = QVBoxLayout()
            layout.addWidget(self.text_box)
            layout.addWidget(self.dpi_text_box)
            layout.addWidget(self.fontsize_text_box)
            layout.addWidget(self.DPILabel)
            layout.addWidget(self.fontsizelabel)
            layout.addWidget(self.view)
            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        def renderticker(self):
            eq = self.text_box.text()
            global DPI
            global FONT_SIZE
            try:
                DPI = int(self.dpi_text_box.text())
                FONT_SIZE = int(self.fontsize_text_box.text())
            except ValueError:
                DPI = 300
                FONT_SIZE = 12
            # Set to 1 if equation failed to render, for safe display
            failFlag = 0
            try:
                render(eq)
            except ValueError:
                print(f'Error in equation: {eq}')
            except Exception as e:
                if e == 'FAILED':
                    failFlag = 1
                    render(r'\text{ }')
            global byteIO
            if failFlag == 0:
                byte_array = QByteArray(byteIO.getvalue())
                mimeData = QMimeData()
                mimeData.setData("image/svg+xml", byte_array)
                clipboard = QGuiApplication.clipboard()
                clipboard.setMimeData(mimeData)

                # Write the SVG data to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".svg") as temp:
                    temp.write(byte_array.data())
                    temp_path = temp.name

                # Load the temporary file into the QGraphicsSvgItem and add it to the scene
                svgItem = QGraphicsSvgItem(temp_path)
                self.scene.clear()  # Clear the previous SVG
                self.scene.addItem(svgItem)
                self.view.fitInView(svgItem, Qt.AspectRatioMode.KeepAspectRatio)  # Keep the aspect ratio

                byteIO.seek(0)
                byteIO.truncate()


    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
