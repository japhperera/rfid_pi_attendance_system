import cv2
from PIL import Image

# initialize the camera
cam = cv2.VideoCapture(0)
ret, image = cam.read()
print("video Object Created")
if ret:
    cv2.imshow('SnapshotTest',image)
    cv2.waitKey(0)
    cv2.destroyWindow('SnapshotTest')
    cv2.imwrite('/home/pi/webcam/SnapshotTest.jpg',image)
cam.release()
print("End of the Function")
