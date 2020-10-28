from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
import os
from os import path
import sys
import urllib.request
from PyQt5.QtWidgets import QMessageBox
import pafy
import humanize


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        uic.loadUi('main.ui', self)
        self.handel_ui()
        self.handel_button()

    def handel_ui(self):
        self.setWindowTitle("MH Downloud ")
        self.setFixedSize(600, 330)

    def handel_browes(self):
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory=".", filter="All Files(*.*)")
        print(save_location)
        self.lineEdit_2.setText(str(save_location[0]))

    def handel_button(self):
        self.pushButton_2.clicked.connect(self.downloud)
        self.pushButton.clicked.connect(self.handel_browes)
        self.pushButton_5.clicked.connect(self.Get_Video_Data)
        self.pushButton_4.clicked.connect(self.Download_Video)
        self.pushButton_3.clicked.connect(self.Save_Browse)

    def handel_progres(self, blocknum, blocksize, totalsize):
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            # QApplication.processEvents()

    def downloud(self):
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(
                url, save_location, self.handel_progres)
        except Exception:
            QMessageBox.information(self, "Error Massege", "Downloud faild")
            return
        QMessageBox.information(self, "Downloud Compled", "Finsh Downloud")
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    def Save_Browse(self):
        # save location in the line edit
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_3.setText(str(save_location[0]))

    def Get_Video_Data(self):

        video_url = self.lineEdit_4.text()
        print(video_url)

        if video_url == '':
            QMessageBox.warning(self, "Data Error",
                                "Provide a valid Video URL")

        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

            video_streams = video.videostreams
            for stream in video_streams:
                print(stream.get_filesize())
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} {}".format(
                    stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox.addItem(data)

    def Download_Video(self):
        video_url = self.lineEdit_4.text()
        save_location = self.lineEdit_3.text()

        video = pafy.new(video_url)
        video_stream = video.videostreams
        video_quality = self.comboBox.currentIndex()
        download = video_stream[video_quality].download(
            filepath=save_location)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
