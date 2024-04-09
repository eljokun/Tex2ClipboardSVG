# TESTED IN PYTHON 3.12, CANNOT GUARANTEE COMPATIBILITY WITH OLDER VERSIONS
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLineEdit
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QMimeData, QByteArray, Qt, QObject
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QLabel
import tempfile
import sys
import io
import matplotlib.pyplot as plot

# Declare that we're using math text for matplotlib
plot.rc('mathtext', fontset='cm')

# Prepare byte I/O stream for image data to be transferred to clipboard


class Properties(QObject):
    def __init__(self):
        super().__init__()
        self.byteIO = io.BytesIO()  # SVG

        # Declare defaults
        self.DPI = 300
        self.FONT_SIZE = 12

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.properties = Properties()


        self.text_box = QLineEdit(self)
        self.text_box.setPlaceholderText("Input Equation [TeX]")
        self.text_box.textChanged.connect(self.renderticker)
        self.dpi_text_box = QLineEdit(self)
        self.dpi_text_box.setPlaceholderText("DPI - Default is 300 DPI")
        self.dpi_text_box.textChanged.connect(self.renderticker)
        self.fontsize_text_box = QLineEdit(self)
        self.fontsize_text_box.setPlaceholderText("Font Size [pt] - Default is 12")
        self.fontsize_text_box.textChanged.connect(self.renderticker)
        self.DPILabel = QLabel(f'Resolution: {self.properties.DPI} DPI')
        self.fontsizelabel = QLabel(f'Font size: {self.properties.FONT_SIZE} pt')
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
        self.render_equation(
            r'\iint_{T} \; \left| \dfrac{\partial \vec{v}(t,s)}{\partial t} \times '
            r'\dfrac{\partial \vec{v}(t,s)}{\partial s}\right|')


    def render_equation(self, equation):
        # # Get byte IO as global duh
        # global byteIO
        # # get global user-defined or default DPI and font size
        # global DPI
        # global FONT_SIZE
        # # matplotlib stuff lol
        try:
            # Initialize plot

            img = plot.figure(figsize=(1, 1))
            img.text(0, 0, fr"${equation.rstrip()}$", parse_math=True)

            # Create SVG of plot, save as byte stream instead of file
            img.savefig(self.properties.byteIO, dpi= self.properties.DPI, transparent=True, format='svg', bbox_inches='tight', pad_inches=0.1)
            plot.close(img)
        except Exception:
            import traceback
            traceback.print_exc()
    def renderticker(self):
        eq = self.text_box.text()
        if not eq: return  # make sure it's not empty
        # global DPI
        # global FONT_SIZE
        try:
            self.properties.DPI = int(self.dpi_text_box.text())
            self.properties.FONT_SIZE = int(self.fontsize_text_box.text())
        except ValueError:
            self.properties.DPI = 300
            self.properties.FONT_SIZE = 12
        # Set to 1 if equation failed to render, for safe display
        failFlag = 0
        try:
            self.render_equation(eq)
        except ValueError:
            print(f'Error in equation: {eq}')
        except Exception as e:
            if e == 'FAILED':
                failFlag = 1
                self.render_equation(r'\text{ }')
        # global byteIO
        if failFlag == 0:
            byte_array = QByteArray(self.properties.byteIO.getvalue())
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

            self.properties.byteIO.seek(0)
            self.properties.byteIO.truncate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

''' IGNORE: REWRITING THE ENTIRE PROGRAM AS A TEST. EXPERIMENTAL
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLineEdit
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QMimeData, QByteArray, Qt, QObject
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QLabel
import tempfile
import sys
import io
import matplotlib.pyplot as plot

 # u should have this in a separate git branch
 # well self is important in python, it the way to access class props
 # cuz rn you're just using globul variables which is catastrophically bad
 # so what else u want me to help with then
 # will check for any other problems
 # and more classes, spreading things out gut
 # you have everything in mainWindow
 # preferably, we'd have a class that's just the ui, one that's the props, and one that connects everying
 # you want more py files? DON'T MIND IF I DO
 # 
 # no it wouldn't, just need to get used to dir structure
 # then it better be good
 # also i  thiinkk im going to copy gwen directory structure and stuff
 # maybe the build tooling too so it's QUICK AND EASY so noobs don't have to install python, just run exe
 # how's that?
 
 
 more files would be neater tbh
 # we could refactor with ur self shit i guess
 # reminder this is for academics or note takers who just want a quick equation to be rendered
def renderTeX(equation):
    global DPI
class MainWindow(QMainWindow):
    DPI = 300
    FONT_SIZE = 12




'''

