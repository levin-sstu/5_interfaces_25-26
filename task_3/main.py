import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QComboBox, QFileDialog, QMessageBox
)
from PyQt5.QtMultimedia import QAudioRecorder, QAudioEncoderSettings, QMediaRecorder, QMediaPlayer, QMediaContent, \
    QVideoEncoderSettings
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture
from PyQt5.QtCore import QUrl, QDir
import os

os.environ['QT_PLUGIN_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Lib', 'site-packages',
                                            'PyQt5', 'Qt5', 'plugins')


class RecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio/Video Recorder")
        self.resize(400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Audio", "Video"])
        self.layout.addWidget(self.mode_selector)

        self.record_button = QPushButton("Start Recording")
        self.record_button.clicked.connect(self.toggle_recording)
        self.layout.addWidget(self.record_button)

        self.play_button = QPushButton("Play Recording")
        self.play_button.clicked.connect(self.play_recording)
        self.layout.addWidget(self.play_button)

        self.save_button = QPushButton("Save Recording")
        self.save_button.clicked.connect(self.save_recording)
        self.layout.addWidget(self.save_button)

        self.recorder = None
        self.is_recording = False
        self.output_file_path = None
        self.player = QMediaPlayer()

    def toggle_recording(self):
        if not self.is_recording:
            mode = self.mode_selector.currentText()
            if mode == "Audio":
                self.start_audio_recording()
            elif mode == "Video":
                self.start_video_recording()
            self.record_button.setText("Stop Recording")
        else:
            self.stop_recording()
            self.record_button.setText("Start Recording")

    def start_audio_recording(self):
        self.recorder = QAudioRecorder()
        audio_settings = QAudioEncoderSettings()
        audio_settings.setCodec("audio/wav")
        self.recorder.setAudioSettings(audio_settings)
        self.output_file_path = QDir.tempPath() + "/output_audio.wav"
        self.recorder.setOutputLocation(QUrl.fromLocalFile(self.output_file_path))
        self.recorder.record()
        self.is_recording = True
        print(f"Audio recording started. File will be saved to: {self.output_file_path}")

    def start_video_recording(self):
        try:
            self.camera = QCamera()
            self.recorder = QMediaRecorder(self.camera)

            # Set video encoder settings
            video_settings = QVideoEncoderSettings()
            video_settings.setCodec("video/h264")
            self.recorder.setVideoSettings(video_settings)

            # Set audio encoder settings (for video)
            audio_settings = QAudioEncoderSettings()
            audio_settings.setCodec("audio/aac")
            self.recorder.setAudioSettings(audio_settings)

            self.output_file_path = QDir.tempPath() + "/output_video.mp4"
            self.recorder.setOutputLocation(QUrl.fromLocalFile(self.output_file_path))

            self.camera.start()
            self.recorder.record()
            self.is_recording = True
            print(f"Video recording started. File will be saved to: {self.output_file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start video recording: {str(e)}")

    def stop_recording(self):
        if self.recorder:
            self.recorder.stop()
        if hasattr(self, 'camera') and self.camera:
            self.camera.stop()
        self.is_recording = False
        print(f"Recording stopped. File saved to: {self.output_file_path}")

    def play_recording(self):
        if not self.output_file_path or not QDir().exists(self.output_file_path):
            QMessageBox.warning(self, "Warning", "No recording to play!")
            return

        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.output_file_path)))
        self.player.setVolume(100)
        self.player.play()

    def save_recording(self):
        if not self.output_file_path or not QDir().exists(self.output_file_path):
            QMessageBox.warning(self, "Warning", "No recording to save!")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Recording", "",
                                                   "Audio Files (*.wav);;Video Files (*.mp4)")
        if save_path:
            try:
                with open(self.output_file_path, 'rb') as src:
                    with open(save_path, 'wb') as dest:
                        dest.write(src.read())
                QMessageBox.information(self, "Info", f"Saved to: {save_path}")
                print(f"Recording saved to: {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecorderApp()
    window.show()
    sys.exit(app.exec_())
