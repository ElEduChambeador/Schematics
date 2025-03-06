import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QLineEdit, QFrame, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

class LinkPreviewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Link Previewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QFrame()
        self.setCentralWidget(self.central_widget)

        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.browser)

        self.link_entry = QLineEdit()
        self.link_entry.returnPressed.connect(self.preview_link)
        self.central_layout.addWidget(self.link_entry)

    def preview_link(self):
        link = self.link_entry.text()
        if link:
            url = QUrl(link)
            self.browser.setUrl(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LinkPreviewer()
    window.show()
    sys.exit(app.exec_())
