import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
from NewTest import Ui_MainWindow
from PyQt5.QtGui import QPixmap

# cài dùng lệnh pip install tensorflow-cpu
import tensorflow.keras
# cài dùng lệnh pip install pillow
from PIL import Image, ImageOps
# cài dùng lệnh pip install numpy
import numpy as np

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        #khai bao nut an
        self.uic.Browser_button.clicked.connect(self.linkto)
        #khai bao nut scan anh
        self.uic.Start_Button.clicked.connect(self.Scanpic)

    def Scanpic(self):
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        model = tensorflow.keras.models.load_model('keras_model.h5')

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        image = Image.open(linkpic)

        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # display the resized image
        #image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        print(prediction)

        # khai bao thu vien ten ca sy
        name = ['celena','taylor']
        # tim vi tri so lon nhat trong mang
        position_1 = prediction.argmax()
        # tim so lon nhat trong mang
        max_value_1 = np.amax(prediction)
        # trinh dien ten ca sy thu 1
        self.uic.Name_1.setText('name: '+str(name[position_1]))
        # trinh dien phan tram chinh xac cua ca sy thu 1
        self.uic.Percent_1.setText(str(round(max_value_1*100,2))+' %')

        # tìm ca sỹ có phần trăm đúng thứ 2
        # copy dữ liệu prediction
        AA = prediction.copy()
        # tìm vị trí số lớn nhất trong AA
        position_2 = AA.argmax()
        # thay giá trị số lớn nhất vừa tìm được
        AA[0][position_2] = 0
        # vi tri so lon nhat sau khi da thay gia tri
        position_3 = AA.argmax()
        # gia tri lon nhat trong mang 2D
        max_value_2 = np.amax(AA)
        print(AA)
        # trinh dien ten ca sy so 2
        self.uic.Name_2.setText('name: '+str(name[position_3]))
        # trinh dien phan tram cua ca sy so 2
        self.uic.Percent_2.setText(str(round(max_value_2*100,3))+' %')

    def linkto(self):
        # tim duong dan
        link = QFileDialog.getOpenFileName(filter='*.jpg *.png')
        # mo hinh len
        self.uic.Screen.setPixmap(QPixmap(link[0]))
        # hien duong truyen len tren line edit
        self.uic.line_Edit.setText(link[0])
        # # lay link tren man hinh line_Edit
        global linkpic
        linkpic = self.uic.line_Edit.text()
        # # global linkchange
        # global linkchange
        # # thay the ky tu tren link
        # linkchange = linkpic.replace('/','//')


    def show(self):
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

