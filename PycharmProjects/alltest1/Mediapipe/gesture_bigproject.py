# 识别手势
import cv2
import mediapipe as mp
import math

# 基本操作写了先
mp_drawing = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# 计算两个向量的夹角，公式计算arc cos cos
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 180
    return angle_


# 手指的角度
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
    )
    '''
    解释：关节点：hand_的第一个空代表关节点，第二个空代表 x or y, 0对应x，1对应y
    把它们当成两个向量，计算其夹角
    '''
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
    )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
    )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
    )
    angle_list.append(angle_)
    return angle_list


# 根究不同手指的角度，返回对应的手势
def gesture(finger_angle):
    f1 = finger_angle[0]  # 大拇指角度
    f2 = finger_angle[1]  # 食指角度
    f3 = finger_angle[2]  # 中指角度
    f4 = finger_angle[3]  # 無名指角度
    f5 = finger_angle[4]  # 小拇指角度
    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮；全张开就趋于0度
    if f1 >= 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return "rock"
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        return "scissors"
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return "paper"
    # if f1 < 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
    #     return 'good'
    # elif f1 >= 50 and f2 >= 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
    #     return 'no!!!'
    # elif f1 < 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 < 50:
    #     return 'ROCK!'
    # elif f1 >= 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
    #     return '0'
    # elif f1 >= 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 < 50:
    #     return 'pink'
    # elif f1 >= 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
    #     return '1'
    # elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
    #     return '2'
    # elif f1 >= 50 and f2 >= 50 and f3 < 50 and f4 < 50 and f5 < 50:
    #     return 'ok'
    # elif f1 < 50 and f2 >= 50 and f3 < 50 and f4 < 50 and f5 < 50:
    #     return 'ok'
    # elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 > 50:
    #     return '3'
    # elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 < 50:
    #     return '4'
    # elif f1 < 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 < 50:
    #     return '5'
    # elif f1 < 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 < 50:
    #     return '6'
    # elif f1 < 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
    #     return '7'
    # elif f1 < 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
    #     return '8'
    # elif f1 < 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 >= 50:
    #     return '9'
    # else:
    #     return ''


cap = cv2.VideoCapture(0)
fontFace = cv2.FONT_HERSHEY_SIMPLEX
lineType = cv2.LINE_AA

with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        # max_num_hands=1,
        min_tracking_confidence=0.5
) as hands:
    if not cap.isOpened():
        print('wrong')
        exit()
    w, h = 540, 310  # 图像的尺寸
    while cap.isOpened():
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (w, h))
        if not ret:
            print('wrong')
            break
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img2)  # 得到侦测手势的结果
        # 画追踪手部的线条
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_points = []  # 储存手指的坐标
                for i in hand_landmarks.landmark:
                    x = i.x * w  # 这里乘w, h可以理解为线性变换
                    y = i.y * h
                    finger_points.append((x, y))
                if finger_points:
                    finger_angle = hand_angle(finger_points)
                    text = gesture(finger_angle)
                    cv2.putText(img, text, (30, 120), fontFace, 5, (255, 255, 255), 10, lineType)
                # 手的轮廓
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_style.get_default_hand_landmarks_style(),
                    mp_drawing_style.get_default_hand_connections_style()
                )
        cv2.imshow('test', img)
        if cv2.waitKey(5) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
