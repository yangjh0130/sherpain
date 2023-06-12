import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from getpass import getpass
import urllib3
import smtplib                             
from email.mime.text import MIMEText
import argparse


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

####
fw_ip = '192.168.20.250'
fw_id = 'admin'
fw_pw = 'password'
####


def key():
    
    url = "https://"+fw_ip+"/api/?"
    params = {"type": "keygen", "user":fw_id, "password": fw_pw}

    response = requests.get(url, params=params, verify = False)

    root = ET.fromstring(response.content)
    apikey = root[0][0].text

    return(apikey)


def object():

    headers = {"X-PAN-KEY": key()}

    url = "https://"+fw_ip+"/restapi/v10.2/Objects/Schedules"
    params = {"location": "vsys", "vsys": "vsys1"}

    response = requests.get(url, params=params, verify = False, headers=headers)

    json_object = json.loads(response.text)
    json_formatted_str = json.dumps(json_object, indent=2)

    json_value = json.loads(json_formatted_str)
    find_dict = json_value["result"]["entry"]
    result_dict = list(member["schedule-type"]["non-recurring"]["member"] for member in find_dict)

    b=0
    for a in result_dict:
        a = str(a)
        a = a[19:-8]
        globals()['end_value_'+str(b)] = a
        b+=1

    today = datetime.now()
    today_value = today.strftime("%Y/%m/%d")

    b=0
    while True:
        if 'end_value_'+str(b) in globals():
            b+=1
        else:
            break

    c = []
    for i in globals():
        if i[0:10] == 'end_value_':
            if today_value >= globals()[i]:
                c.append(i[-1])

    d = []
    for hm in c:
        d.append(find_dict[int(hm)]["@name"])

    return(d)
        
      
def rules():

    headers = {"X-PAN-KEY": key()}

    url = "https://"+fw_ip+"/restapi/v10.2/Policies/SecurityRules"
    params = {"location": "vsys", "vsys": "vsys1"}

    response = requests.get(url, params=params, verify = False, headers=headers)
    
    json_object = json.loads(response.text)
    json_formatted_str = json.dumps(json_object, indent=2)
    
    json_value = json.loads(json_formatted_str)
    find_dict = json_value["result"]["entry"]

    schedule_bye = object()
    schedule_value = []

    for i in find_dict:
        try:
            if i["schedule"] is not None:
               schedule_value.append(i["schedule"])
        except:
            continue
    
    f_value = []
    nf_value = []
    r_value = []
    
    for k in schedule_value:
        if k in schedule_bye:
            f_value.append(k)

    for z in f_value:
        if z not in nf_value:
            nf_value.append(z)
    
    for m in nf_value:
        for n in find_dict:
            try:
                if m in n["schedule"]:
                    r_value.append(n["@name"])
            except:
                continue
            
    return(r_value)


def send_mail():
    
    ###
    smtpName = "smtp.office365.com"
    smtpPort = 587
    
    sendEmail = "test@email.com"
    password = "password"
    
    recvEmail = ["test@email.com","test1@email.com"]
    ###
    
    now = datetime.now()
    title = now.strftime("Paloalto %Y년 %m월 %d일 만료 정책".encode('unicode-escape').decode()).encode().decode('unicode-escape')

    if len(rules()) == 0:
        send_message = "만료되는 정책이 없습니다."

    else:
        send_message = rules()
        send_message = str(send_message)
        send_message = send_message.replace(",", " ")
        send_message = send_message.replace("'", "")
        send_message = send_message.strip("[""]")
        send_message = send_message.replace(" ", "\n")

    f_send_message = title + "\n\n\n" + send_message + "\n "
    
    msg = MIMEText(f_send_message)
    msg['From'] = sendEmail
    msg['To'] = ", ".join(recvEmail)
    msg['Subject'] = title

    sm = smtplib.SMTP(smtpName , smtpPort)         
    sm.starttls()                                  
    sm.login(sendEmail , password)                 
    sm.sendmail(sendEmail, recvEmail, msg.as_string())  
    sm.close()   

send_mail()
