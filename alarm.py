# pip3 install opencv-python
# pip install numpy
import cv2
import numpy as np
import time

cameraIndex = 0  # 0 for laptop webcam, 1 for external webcam
saving = False  # save the image (True) or not, only show (False)
looking = True

# https://api.telegram.org/bot5469207488:AAErlmUh1eUV7GTC9v2y3AuNkEHbpR2s1lU/sendMessage?chat_id=5469207488&text='Alarm'


def webcam_read(webcam):
    check, frame = webcam.read()
    print(check)
    print(frame)
    time.sleep(0.5)
    cv2.imshow("Capturing", frame)
    return check, frame


def is_found(img_rgb, template_file):
    template = cv2.imread(template_file)
    w, h = template.shape[:-1]
    found = False

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        found = True
        cv2.rectangle(
            img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    return found, img_rgb, template_file[0]



def main():
    webcam = cv2.VideoCapture(cameraIndex)

    webcam_read(webcam)

    time.sleep(3)

    while looking:
        try:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            camimg = timestr + '.png'
            found = False

            check, frame = webcam_read(webcam)

            if saving:
                cv2.imwrite(filename=camimg, img=frame)  # no need to save file
                img_rgb = cv2.imread(camimg)  # no need to read un-saved file
            else:
                img_rgb = frame

            if not found:
                found, img_rgb, lvl = is_found(img_rgb, '5-1.png')

            if not found:
                found, img_rgb, lvl = is_found(img_rgb, '6-1.png')

            if found == True:
                cv2.imwrite(timestr + '_lvl_' + lvl + '.png', img_rgb)
                txt = ('POLLUTION LVL ' + lvl)
                print(txt)
                telegram_alarm(txt)
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

def telegram_alarm(message):
    pass
    # send message to bot, which will than be sent to all subscribed users

main()
