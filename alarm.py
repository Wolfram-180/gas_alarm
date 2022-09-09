# pip3 install opencv-python
# pip install requests
# pip install pillow
import datetime
import cv2
import numpy as np
import time
import sqlite3
from safe_bot_token import bot_token
import requests
from time import sleep
import io
from PIL import Image

detection_images = ['5.png', '6.png', ]

match_threshold = 0.9  # matching threshold, 1 - perfect match, <1 - less strict

looking = True  # true to check camera at all
saving = False  # save the image (True) or not, only show (False)

cameraIndex = 0  # 0 for laptop webcam, 1 for external webcam
tele_message_count = 5  # count of warning messages to telegram
tele_message_delay_sec = 3  # delay between warning messages to telegram
init_start_delay_sec = 3.0  # delay before start
pause_sec_camera = 1.12  # frequency of checking the camera
end_if_found = False  # end script if warning detected
sleep_if_found_sec = 3  # script sleep if warning detected
alarms_detected = 'alarms_detected'  # folder for screenshots of alarms detected

control_work_time = True # control work time : hr_work_from <-> hr_work_to
hr_work_from = 0
hr_work_to = 7


def webcam_read(webcam):
    check, frame = webcam.read()
    print(check)
    print(frame)
    time.sleep(pause_sec_camera)
    cv2.imshow("Capturing", frame)
    return check, frame


def is_found(img_rgb, template_file):
    template = cv2.imread(template_file)
    w, h = template.shape[:-1]
    found = False

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = match_threshold
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        found = True
        cv2.rectangle(
            img_rgb, pt, (pt[0] + h, pt[1] + w), (0, 0, 255), 2)
    return found, img_rgb, template_file[0]


def main():
    webcam = cv2.VideoCapture(cameraIndex)
    webcam_read(webcam)
    time.sleep(init_start_delay_sec)

    while looking:
        now = datetime.datetime.now()
        try:
            if control_work_time:
                if not (hr_work_from <= now.hour <= hr_work_to):
                    for i in range(0, 60):
                        print(
                            f'Out of control hours: now - {str(now.hour)}, control - from {str(hr_work_from)} to {str(hr_work_to)}; so let`s sleep {i} of 60')
                        sleep(1)
                    continue

            timestr = time.strftime("%Y%m%d-%H%M%S")
            camimg = timestr + '.png'
            found = False

            check, frame = webcam_read(webcam)

            if saving:
                cv2.imwrite(filename=camimg, img=frame)

            img_rgb = frame

            for detection_image in detection_images:
                found, img_rgb, lvl = is_found(img_rgb, detection_image)
                if found:
                    detect_img = detection_image
                    break

            if found:
                alarms_detected_full_path = alarms_detected + \
                    '/' + timestr + '_lvl_' + detect_img
                cv2.imwrite(alarms_detected_full_path, img_rgb)
                txt = ('Pollution level / Уровень загрязнения: ' + lvl)
                print(txt)

                telegram_alarm(lvl, alarms_detected_full_path)

                if end_if_found:
                    webcam.release()
                    cv2.destroyAllWindows()
                    break
                else:
                    print('Sleeping for ' + str(sleep_if_found_sec) + ' seconds')
                    sleep(sleep_if_found_sec)

            key = cv2.waitKey(1)
            if key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break

        except (KeyboardInterrupt):
            webcam.release()
            cv2.destroyAllWindows()
            break


def get_link(bot_token, msgtp, chatId, alarm):
    return f'https://api.telegram.org/bot{bot_token}/send{msgtp}?chat_id={chatId}&text={alarm}'


def telegram_alarm(lvl, alarms_detected_full_path):
    conn = sqlite3.connect("user_info.db")

    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER
        )""")
    conn.commit()

    cursor.execute(f"SELECT id FROM user")
    data = cursor.fetchall()

    alarm = f'Pollution level (6 is max) / Уровень загрязнения (6 макс):  {lvl}'

    img = Image.open(alarms_detected_full_path)

    # save image in memory
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    files = {"photo": img_bytes}

    for chatId in data:
        file_sent = False
        for i in range(0, tele_message_count):
            if not file_sent:
                bot_send_link = get_link(bot_token, 'Photo', chatId[0], alarm)
                print(bot_send_link)
                requests.post(bot_send_link, files=files)
                file_sent = True
            bot_send_link = get_link(bot_token, 'Message', chatId[0], alarm)
            print(bot_send_link)
            requests.post(bot_send_link)
            sleep(tele_message_delay_sec)


main()
