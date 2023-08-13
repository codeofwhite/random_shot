import cv2

cap = cv2.VideoCapture(0)
if cap.isOpened():
    print('success')

else:
    print('wrong!')
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        print('wrong!')
        break
    frame = cv2.cvtColor(frame, 6)
    cv2.imshow('test', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
