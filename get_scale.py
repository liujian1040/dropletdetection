import cv2
import numpy as np



def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 1, (0, 255, 255), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.5,color=(0,255,255), thickness = 1)
        cv2.imshow("image", img)
        
if __name__ == "__main__":        
    img=cv2.imread('0.png') # 图片路径
    scale_percent = 100       # 缩放比例（%）
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    while(1):
        cv2.imshow("image", img)
        if cv2.waitKey(0)&0xFF==5:
            break
    cv2.destroyAllWindows()