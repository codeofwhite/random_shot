# 简单去背景
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils  # mediapipe 繪圖功能
mp_selfie_segmentation = mp.solutions.selfie_segmentation  # mediapipe 自拍分割方法

cap = cv2.VideoCapture(0)
bg = cv2.imread('C:/Users/zhj20/PycharmProjects/alltest1/images/201936.jpg')  # 載入 windows 經典背景
bg = cv2.resize(bg, (1080, 720))

# mediapipe 啟用自拍分割
with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=1) as selfie_segmentation:
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        if not ret:
            print("Cannot receive frame")
            break
        img = cv2.resize(img, (1080, 720))  # 縮小尺寸，加快演算速度
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 將 BGR 轉換成 RGB
        results = selfie_segmentation.process(img2)  # 取得自拍分割結果
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1  # 如果滿足模型判斷條件 ( 表示要換成背景 )，回傳 True
        output_image = np.where(condition, img, bg)
        # 將主體與背景合成，如果滿足背景條件，就更換為 bg 的像素，不然維持原本的 img 的像素

        cv2.imshow('oxxostudio', output_image)
        if cv2.waitKey(5) == ord('q'):
            break  # 按下 q 鍵停止
cap.release()
cv2.destroyAllWindows()
