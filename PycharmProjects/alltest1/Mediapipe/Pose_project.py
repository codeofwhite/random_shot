# 姿势识别&利用姿势识别去背景
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils  # 绘图方法
mp_drawing_style = mp.solutions.drawing_styles  # 绘图样式
mp_pose = mp.solutions.pose  # 检测姿势

cap = cv2.VideoCapture(0)
bg = cv2.imread(
    'C:/Users/zhj20/PycharmProjects/alltest1/images/dcgqi76-77716f27-2863-4080-b554-777e447ca084.png')  # 背景图片
bg = cv2.resize(bg, (520, 300))

# 把姿势检测开起来
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        enable_segmentation=True) as pose:  # enable_segmentation 是选背景
    if not cap.isOpened():
        print('wrong')
        exit()
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            print('wrong')
            break
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (520, 300))
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转成RGB
        results = pose.process(img2)  # 得到姿势侦测的结果
        try:
            # 避免抓不到时报错
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            img = np.where(condition, img, bg)  # 如果满足condition就回传True，回传false的就用bg代替
        except:
            pass
        # 画出骨架，参数填进去就完事
        mp_drawing.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_style.get_default_pose_landmarks_style()
        )
        cv2.imshow('test', img)
        if cv2.waitKey(5) == ord('q'):  # waitKey里不写数字会不动
            break
cap.release()
cv2.destroyAllWindows()
