# 训练人脸
import cv2
import numpy as np

detector = cv2.CascadeClassifier('C:/Users/zhj20/PycharmProjects/alltest1/raw.githubusercontent.com_opencv_'
                                 'opencv_4.x_data_haarcascades_haarcascade_frontalface_default.xml')  # 載入人臉追蹤模型
recog = cv2.face.LBPHFaceRecognizer_create()  # 啟用訓練人臉模型方法
faces = []  # 儲存人臉位置大小的串列
ids = []  # 記錄該人臉 id 的串列

for i in range(1,28):
    img = cv2.imread(f'C:/Users/zhj20/PycharmProjects/alltest1/images/face1/bd{i}.jpg')  # 依序開啟每一張照片
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 色彩轉換成黑白
    img_np = np.array(gray, 'uint8')  # 轉換成指定編碼的 numpy 陣列
    face = detector.detectMultiScale(gray)  # 擷取人臉區域
    for (x, y, w, h) in face:
        faces.append(img_np[y:y + h, x:x + w])  # 記錄蔡拜登人臉的位置和大小內像素的數值
        ids.append(1)  # 記錄id,id只能是整數，都是 1 表示拜登的 id 為 1

print('training...')  # 提示開始訓練
recog.train(faces, np.array(ids))  # 開始訓練
recog.save('face.yml')  # 訓練完成儲存為 face.yml
print('ok!')
