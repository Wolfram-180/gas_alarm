# pip3 install opencv-python
# pip install numpy
# pip install requests
import cv2
import numpy as np
import time
import sqlite3
from safe_bot_token import bot_token
import requests
from time import sleep

cameraIndex = 0  # 0 for laptop webcam, 1 for external webcam
saving = False  # save the image (True) or not, only show (False)
looking = True


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
                telegram_alarm(lvl)
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


def telegram_alarm(lvl):
    conn = sqlite3.connect("user_info.db")

    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER
        )""")
    conn.commit()

    cursor.execute(f"SELECT id FROM user")
    data = cursor.fetchall()

    alarm = f'Внимание! В Видном произошло загрязнение воздуха! Уровень {lvl} из 6'

    for i in range(0, 5):
        for chatId in data:
            bot_send_link = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatId[0]}&text={alarm}'
            requests.get(bot_send_link)
            print(bot_send_link)
            sleep(3)


main()
