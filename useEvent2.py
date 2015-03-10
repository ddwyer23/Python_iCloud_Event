#!/usr/bin/python3.4

import urllib.request
import json
import zlib
import time
import string
import getpass

#  ___________________________________________________________________________
# | iCloud Event Creater                                                      |
# | Author: Devin Dwyer (dpd4466@rit.edu)                                     |
# |---------------------------------------------------------------------------|
# | Utilizes the iCloud Web API to create an event 1 minute past the current  |
# | time. This can be used for logging purposes to send updates to an iPhone. |
# |___________________________________________________________________________|


# ***************
# | loginPacket |
# ***************
# Sends credentials to iCloud and returns the response cookies
# (with authentication token)
def loginRequest():
    i_email = input("Enter iCloud E-mail Address: ")
    i_passwd = getpass.getpass("Enter iCloud Password: ")
    print('Sending login packet')
    header = {'Content-Type': 'text/plain',
               'Host': 'setup.icloud.com',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Referer': 'https://www.icloud.com/',
               'Origin': 'https://www.icloud.com',
               'Connection': 'keep-alive',
               'Accept-Language': 'en-US,en;q=0.8',
               'Accept': '*/*'}
    url = 'https://setup.icloud.com/setup/ws/1/login?clientBuildNumber=14C.131972&clientId=5DB71ED4-E27E-4292-B868-49F213BE64F5'
    raw_data = {"apple_id":i_email, "password":i_passwd, "success": 'false'} # credentials
    serialized_data = json.dumps(raw_data) # serialize data
    payload = str.encode(serialized_data)  # encode data
    print('Sending login packet.')
    request = urllib.request.Request(url, payload, header) # spawn Request
    opened_request = urllib.request.urlopen(request) 
    print('Sending login packet..')
    compr_response = opened_request.read() # read response from opened Request
    response = zlib.decompress(compr_response, 16+zlib.MAX_WBITS) # decompress response data
    cookies = ''
    print('Sending login packet...')
    for i in opened_request.getheaders(): # find and grab cookies
        if i[0] == 'Set-Cookie':
            index = (i[1].index(';') + 1)
            cookies += i[1][:index]
    print('Completed.\n\n')
    return cookies


# ***********
# | getDate |
# ***********
# Creates the formatted list of start/end dates
# for the event payload
def getDate():
    date = []
    date.append(int(time.strftime("%Y%m%d")))
    date.append(int(time.strftime("%Y")))
    date.append(int(time.strftime("%m")))
    date.append(int(time.strftime("%d")))
    date.append(int(time.strftime("%H"))-3) # Subtract 3 from hour to convert to EST
    date.append(int(time.strftime("%M"))+1) # Add 1 minute to the time
    date.append(960)
    return date


# *************
# | sendEvent |
# *************
# Constructs the payload and used the proper cookies (w/ auth token)
# in order to create a POST request for the event
def sendEvent(cookies, title, synopsis):
    url  =  "https://p18-calendarws.icloud.com/ca/events/B247BD44-5E7A-4E34-B28E-0076261C94FB/84A5E014-5D08-4B26-97F8-F8A07CB4C27F?clientBuildNumber=15A99&clientId=2EF49705-0380-4C3B-AA7C-B047F5BEAE6D&clientVersion=5.1&dsid=1793997407&endDate=2015-03-21&lang=en-us&requestID=6&startDate=2015-02-19&usertz=US%2FPacific"
    header = {'Host': 'p18-calendarws.icloud.com',
              'Accept': '*/*',
              'Accept-Encoding': 'gzip, deflate',
              'Origin': 'https://www.icloud.com',
              'Accept-Language': 'en-US,en;q=0.8',
              'Referer': 'https://www.icloud.com/applications/calendar/current/en-us/index.html?',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36',
              'Content-Type': 'text/plain',
              'Connection': 'keep-alive',
              'Cookie': cookies}
    
    startDate = getDate()
    endDate = getDate()
    
    payload = {"Event":{"pGuid":"B247BD44-5E7A-4E34-B28E-0076261C94FB",
                        "extendedDetailsAreIncluded":True,
                        "title":title,"location":synopsis,
                        "localStartDate":startDate,
                        "localEndDate":endDate,
                        "startDate":startDate,
                        "endDate":endDate,
                        "allDay":False,"duration":1,"guid":"84A5E014-5D08-4B26-97F8-F8A07CB4C27F","tz":"US/Pacific",
                        "recurrenceMaster":False,"recurrenceException":False,"icon":0,"hasAttachments":False,
                        "alarms":["84A5E014-5D08-4B26-97F8-F8A07CB4C27F:3BED7FF5-2F72-4051-9AE9-95FD44CBE47A"],
                        "changeRecurring":0},
               "Alarm":[{"guid":"84A5E014-5D08-4B26-97F8-F8A07CB4C27F:3BED7FF5-2F72-4051-9AE9-95FD44CBE47A",
                         "pGuid":"84A5E014-5D08-4B26-97F8-F8A07CB4C27F","measurement":{"before":False,"weeks":0,"days":0,"hours":0,"minutes":0,"seconds":0},
                         "description":"Event reminder","messageType":"message"}],
               "ClientState":{"Collection":[{"guid":"B247BD44-5E7A-4E34-B28E-0076261C94FB",
                                             "ctag":"FT=-@RU=183ccfef-7e2a-4aaa-80d9-2340864b4158@S=57"}],
                              "fullState":False,"userTime":1234567890,"alarmRange":1}}
    
    payload = json.dumps(payload)
    payload = str.encode(payload)
    request = urllib.request.Request(url, data=payload, headers=header)
    opened_request = urllib.request.urlopen(request)
    read = opened_request.read()
    response = zlib.decompress(read, 16+zlib.MAX_WBITS)
    print(response)    

def main():    
	cookies = loginRequest()
	title = "Hi"
	synopsis = ""
	sendEvent(cookies, title, synopsis)

main()
