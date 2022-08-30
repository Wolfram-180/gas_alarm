from time import sleep
import cv2
import numpy as np

img_rgb = cv2.imread('full5.png')
template = cv2.imread('p5-4.png')
w, h = template.shape[:-1]

rslt = False

res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
threshold = .5
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    rslt = True
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

if rslt == True:
    cv2.imwrite('result_yes.png', img_rgb)
    print('========= FOUND =========')
else:
    print('========= NOT FOUND =========')
