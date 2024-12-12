import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QFileDialog
import os

os.environ['QT_PLUGIN_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Lib', 'site-packages',
                                            'PyQt5', 'Qt5', 'plugins')

import vlc

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простой видеоплеер")
        self.setGeometry(100, 100, 800, 600)

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.video_widget = QWidget(self)
        self.video_widget.setGeometry(10, 10, 780, 500)
        self.player.set_hwnd(int(self.video_widget.winId()))

        self.open_button = QPushButton("Выбрать файл", self)
        self.open_button.setGeometry(10, 520, 120, 30)
        self.open_button.clicked.connect(self.open_file)

        self.play_button = QPushButton("Пуск", self)
        self.play_button.setGeometry(140, 520, 120, 30)
        self.play_button.clicked.connect(self.play_video)

        self.pause_button = QPushButton("Пауза", self)
        self.pause_button.setGeometry(270, 520, 120, 30)
        self.pause_button.clicked.connect(self.pause_video)

        self.stop_button = QPushButton("Стоп", self)
        self.stop_button.setGeometry(400, 520, 120, 30)
        self.stop_button.clicked.connect(self.stop_video)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать видеофайл", "", "Видео файлы (*.mp4 *.avi *.mkv)")
        if file_name:
            print(f"Selected file: {file_name}")
            self.media = self.instance.media_new(file_name)
            self.player.set_media(self.media)

    def play_video(self):
        self.player.play()

    def pause_video(self):
        self.player.pause()

    def stop_video(self):
        self.player.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
