# 人脸识别基础
import cv2

img = cv2.imread('C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/images/wp1890591.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 將圖片轉成灰階

face_cascade = cv2.CascadeClassifier(
    "C:/Users/zhj20/pycharm_projects/PycharmProjects/alltest1/opencv_/raw.githubusercontent.com_opencv_opencv_4.x_data_haarcascades_haarcascade_frontalface_default.xml")  # 載入人臉模型
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2)  # 偵測人臉
# 偵測並取出相關屬性
# img 來源影像，建議使用灰階影像
# scaleFactor 前後兩次掃瞄偵測畫面的比例係數，預設 1.1
# minNeighbors 構成檢測目標的相鄰矩形的最小個數，預設 3
# flags 通常不用設定，若設定 CV_HAAR_DO_CANNY_PRUNING 會使用 Canny 邊緣偵測，排除邊緣過多或過少的區域
# minSize, maxSize 限制目標區域的範圍，通常不用設定

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 利用 for 迴圈，抓取每個人臉屬性，繪製方框

cv2.imshow('oxxostudio', img)
cv2.waitKey(0)  # 按下任意鍵停止
cv2.destroyAllWindows()
