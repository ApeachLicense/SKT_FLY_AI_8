import numpy as np
import cv2

orange, blue, cyan = (0,165,255), (255,0,0),(255,255,0)
white, black, green, magenta = (255,255,255), (0,0,0),(0,255,0),(255,0,255)

image = np.full((400,600,3),white,np.uint8)

center = (300,200)
pt1, pt2 = (200,100),(450,300)
shade = (pt2[0]+2,pt2[1]+2)
size = (150,80)

cv2.circle(image,center,100,blue)
cv2.circle(image,pt1,50,orange,2)
cv2.circle(image,pt2,70,cyan,-1)

cv2.ellipse(image,pt1,size,0,0,369,green,2)
cv2.ellipse(image,pt2,size,45,0,360,green,2)

cv2.ellipse(image,pt1,size,0,30,270,orange,4)
cv2.ellipse(image,pt2,size,45,-45,90,cyan,4)

font = cv2.FONT_HERSHEY_COMPLEX
cv2.putText(image,"Hello World",(200,200),font,1.0,green,2)
cv2.putText(image,"Hello World",(4,200),font,1.0,green,2)

title = "Draw Circles"
cv2.namedWindow(title)
cv2.imshow(title,image)
cv2.waitKey(0)
cv2.destroyAllWindows()