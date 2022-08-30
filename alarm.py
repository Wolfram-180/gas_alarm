from time import sleep
import cv2
import numpy as np
import time

webcam = cv2.VideoCapture(1)

while True:
    try:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        camimg = timestr + '.png'
        found = False
        check, frame = webcam.read()
        print(check)
        print(frame)

        sleep(1.5)

        cv2.imshow("Capturing", frame)

        cv2.imwrite(filename=camimg, img=frame)  # no need to save file
        img_rgb = cv2.imread(camimg)  # no need to read un-saved file

        # img_rgb = frame

        template = cv2.imread('p5-1.png')
        w, h = template.shape[:-1]

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            found = True
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        template = cv2.imread('p6-1.png')
        w, h = template.shape[:-1]

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            found = True
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        if found == True:
            cv2.imwrite('result_yes.png', img_rgb)
            print('========= FOUND =========')
            webcam.release()
            cv2.destroyAllWindows()
            break

        key = cv2.waitKey(1)
        if key == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break

    except (KeyboardInterrupt):
        webcam.release()
        cv2.destroyAllWindows()
        break
