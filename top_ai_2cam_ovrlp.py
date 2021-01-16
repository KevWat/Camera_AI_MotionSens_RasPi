#!python3.7
# config: UTF-8

import RPi.GPIO as GPIO
import time
import fnc_slack_upload as slk_upl # Upload Slack
import fnc_auto_del as at_del # Old file Auto Delete
import fnc_cap_img_opcv_2camera as cap_opcv # 2 Camera Capture
import fnc_add_ovrl_datetime as ovrl_dt
import fnc_ai_cap as ai_cap

################################
# Object Detect & Capture
################################
BTN = 26 # GPIO BT Number, GPIO 26
path = 'pic/' # Picture Folder Location

capd_img_list = []
#define callback function
def switch_callback(sens_detect):
    if (sens_detect == BTN):
        ## Capture Image
        # Camera Capture
        capd_img_list = cap_opcv.capture_camera(path, 640, 480) # Argument(Save Location,Width, Height), return: captured file name
        #print(capd_img_list)
        time.sleep(1)
        ## Overlay datetime and Upload each img ##
        for capd_img in capd_img_list:
                # Overlay Date Time
                ovrl_dt.add_ovrl_datetime(capd_img)
                # AI: Object Detection *No return data, just over-write
                ai_cap.ai_obj_det(capd_img_list)
                ## Upload on Slack ##
                slk_upl.slack_upload(capd_img)
                print(capd_img)

        ## Delete Old File ##
        at_del.auto_delete_file(path)
        time.sleep(30) # privent to shoot many pics
        print("Cycle Done")
            
   
GPIO.setmode(GPIO.BCM) #Set BCM number to access GPIO
GPIO.setup(BTN, GPIO.IN) #BCM No.26pin

GPIO.add_event_detect(BTN, GPIO.RISING,bouncetime=100) #bounce to prevent chattering
GPIO.add_event_callback(BTN, switch_callback)

try:
    while True:
        #print("No Detect")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()

