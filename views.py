import numpy as np

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QSlider

from pyqtgraph import ImageView


class StartWindow(QMainWindow):
    def __init__(self, camera=None):
        super().__init__()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 10)
        self.slider.valueChanged.connect(self.update_brightness)

        self.camera = camera

        self.central_widget = QWidget()
        self.button_frame = QPushButton('Acquire Frame', self.central_widget)
        self.button_movie = QPushButton('Start Movie', self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_frame)
        self.layout.addWidget(self.button_movie)
        self.layout.addWidget(self.slider)
        self.setCentralWidget(self.central_widget)

        self.button_frame.clicked.connect(self.update_image)

        self.image_view = ImageView()
        self.layout.addWidget(self.image_view)

        # self.button_movie.clicked.connect(self.start_movie)

    # def start_movie(self):
    # self.movie_thread = MovieThread(self.camera)
    # self.movie_thread.start()

    def update_image(self):
        frame = self.camera.get_frame()
        self.image_view.setImage(frame.T)

    def update_brightness(self, value):
        value /= 10
        self.camera.set_brightness(value)


class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.movie_thread = None
        self.camera = camera
        self.button_movie.clicked.connect(self.start_movie)

    def run(self):
        self.camera.acquire_movie(200)

    def start_movie(self):
        self.movie_thread = MovieThread(self.camera)
        self.movie_thread.start()
