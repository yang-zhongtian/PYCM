import cv2
cap = cv2.VideoCapture('udp://225.2.2.21@192.168.1.30:4092', cv2.CAP_FFMPEG)
if not cap.isOpened():
    print('VideoCapture not opened')

while True:
    ret, frame = cap.read()
    if not ret:
        print('frame empty')
        break
    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
    print(cap.get(cv2.CAP_PROP_FPS))

cap.release()
cv2.destroyAllWindows()
