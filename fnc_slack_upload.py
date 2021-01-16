#!python3.7
# config: UTF-8

import requests

################################
# Upload on Slack
################################


#Upload Captured File
def slack_upload(filename):
    # Read Slack's token, channels
    f = open('../../config_slk.txt', 'r')
    data_lines = f.readlines() # Line0 = token, Line1 = channels
    f.close()
    
    url = "https://slack.com/api/files.upload"
    data = {
        
        "token": "xoxb-1302951648786-1303876717379-22L2deFGinNkB4rnKswAtQRY",
        "channels": "cats3",
        
        #"token": data_lines[0],
        #"channels": data_lines[1],
        
        "title": "Today's Picture"
        }
    files = {'file': open(filename, 'rb')}
    requests.post(url, data=data, files=files)
    print("Done: File Upload")

################################

''
