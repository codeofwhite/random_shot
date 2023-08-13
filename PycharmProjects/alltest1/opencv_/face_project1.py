# 识别人脸加马赛克
import cv2

cap = cv2.VideoCapture(0)  # 开启摄像头
face_cascade = cv2.CascadeClassifier(
    "C:/Users/zhj20/PycharmProjects/alltest1/raw.githubusercontent."
    "com_opencv_opencv_4.x_data_haarcascades_haarcascade_frontalface_default.xml")  # 載入OPENCV人臉模型
if not cap.isOpened():  # 如果开不起
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()  # 获取两个参数，一个是成功与否，一个是图像
    frame = cv2.flip(frame, 1)  # 镜像反转
    if not ret:
        print("Cannot receive frame")
        break
    frame = cv2.resize(frame, (540, 320))  # 縮小尺寸，避免尺寸過大導致效能不好
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 將鏡頭影像轉換成灰階
    faces = face_cascade.detectMultiScale(gray)  # 偵測人臉,把上面那个灰阶导入
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 標記人臉，那个框框
        # 马赛克
        # mosaic = frame[y:y + h, x:x + w]
        # level = 15
        # mh = int(h / level)
        # mw = int(w / level)
        # mosaic = cv2.resize(mosaic, (mw, mh), interpolation=cv2.INTER_LINEAR)
        # mosaic = cv2.resize(mosaic, (w, h), interpolation=cv2.INTER_NEAREST)
        # frame[y:y + h, x:x + w] = mosaic
    cv2.imshow('oxxostudio', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
