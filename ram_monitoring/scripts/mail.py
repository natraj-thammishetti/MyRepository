import smtplib
import sys
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

def send_mail(filename,message,recipients):
    sender_email = "natrajthammishetti@gmail.com"
    body = open(filename).read()
    msg = MIMEMultipart()
    delim = ","
    
    temp = list(map(str, recipients))
    res = delim.join(temp)

    print("The resultant string : " + str(res))
    msg['Subject'] = message
    msg['From'] = sender_email
    msg['To'] = res
    msgText = MIMEText(body, 'html')
    msg.attach(msgText)

    try:
        with smtplib.SMTP('smtp.abbvienet.com') as smtpObj:
            smtpObj.sendmail(sender_email, recipients, msg.as_string())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    
    print("Opening the variable file...")
    with open(sys.argv[1]) as variable_file:
        variables = json.load(variable_file)
        
    environment = variables['environment']
    recipients = variables['recipients']
   
    variable_file.close() 
    with open(r"warning.log", 'r') as fp:
        lines = len(fp.readlines())
        filename = "warning.log"
        message="WARNING! ARCH "+environment+" EC2 Instances Disk Usage > 70%"
        if lines > 0:
            send_mail(filename,message,recipients)
    with open(r"critical.log", 'r') as fp:
        lines = len(fp.readlines())
        filename = "critical.log"
        message="CRITICAL! ARCH "+environment+" EC2 Instances Disk Usage > 80%"
        if lines > 0:
            send_mail(filename,message,recipients)
