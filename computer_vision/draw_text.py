import numpy as np
import cv2

olive, violet, brown, blue, red = (128,128,0), (221,160,221), (42,42,165), (255,0,0), (0,0,255)

pt1, pt2 = (50,150), (50,250)

image = np.zeros((400,600,3),np.uint8)
image.fill(255)

cv2.putText(image,"HELLO",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,blue,2)
cv2.putText(image,"WORDL",(50,200),cv2.FONT_HERSHEY_DUPLEX,1,red,2)
cv2.putText(image,"OPEN CV",pt1,cv2.FONT_HERSHEY_SIMPLEX,3,violet,2)
fontFace = cv2.FONT_HERSHEY_PLAIN | cv2.FONT_ITALIC
cv2.putText(image,"PYTHON",pt2,fontFace,3,olive,2)

cv2.imshow("PUT Text",image)
cv2.waitKey(0)
cv2.destroyAllWindows()