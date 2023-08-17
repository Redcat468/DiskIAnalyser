import os
import openai
import smtplib
from email.mime.text import MIMEText

# ------- Configuration SMTP -------
SMTP_SERVER = "enter_your-mailserver"
SMTP_PORT = 465 # Choose port
SMTP_USER = "enter_the_sender_mail"
SMTP_PASSWORD = "enter_the_sender_mail_password"
EMAIL_RECEIVER = "enter_the_receiver_here"

# ------- Configuration OpenAI -------
openai.api_key = 'api_key_here'

# ------- Partie récupération des logs SMART -------
LOG_DIR = "choose_a_dir_to_put_the_smart_reports"
import os
import subprocess
os.makedirs(LOG_DIR, exist_ok=True)
import glob
file_list = glob.glob(f"{LOG_DIR}/*.txt")
for file in file_list:
    os.remove(file)
import subprocess
disks = subprocess.check_output("smartctl --scan | grep scsi", shell=True).decode().splitlines()
count = 1
for disk in disks:
    print("Extractions des rapports smart... "+str(count)+" rapports créés" )
    count=count+1
    disk_name = disk.split()[0]
    log_file = os.path.join(LOG_DIR, f"smart_logs_{disk_name.replace('/', '_')}.txt")
    os.system(f"smartctl --all {disk_name} | head -n 13 | tail -n 9 >> {log_file}")
    log_file = os.path.join(LOG_DIR, f"smart_logs_{disk_name.replace('/', '_')}.txt")
    os.system(f"smartctl --all {disk_name} | head -n 86 | tail -n 27 | awk '{{print $2,$4,$5,$6,$10}}' | column -t -s ' ' >> {log_file}")
    
# ------- Partie analyse -------
import os
import datetime

def analyze_smart_data():
    count = 1
    for log_file in os.listdir(LOG_DIR):
        if log_file.endswith('.txt'):
            with open(os.path.join(LOG_DIR, log_file), 'r') as f:
                log_content = f.read()
                
        import requests

        # Remplacez 'YOUR_API_KEY' par votre clé d'API GPT-3
        api_key = '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'
        url = 'https://api.openai.com/v1/chat/completions'
        
#----- Un peu de mise en forme pour séparer les infos dans le rapport
        with open("rapport.txt", "a") as f:
            f.write("\n\n")
            f.write("- - - - - - - - - - - - - - ")
            f.write("\n\n")
            
#---- Récuperer dans le nom du rapport le nom de device
        file_name = os.path.splitext(os.path.basename(log_file))[0]
        last_underscore_index = file_name.rfind('_')
        characters_after_last_underscore = file_name[last_underscore_index + 1:]
        
        with open("rapport.txt", "a") as f:
            f.write("Disk : " + characters_after_last_underscore)
            f.write("\n")
        
#---- Récuperer dans le rapport les infos du disque      
        with open(log_file, 'r') as f:
            import re
            for line in f:
                if re.match(r"(Model Family|Device Model|Serial Number)", line):
                    with open("rapport.txt", "a") as f:
                        f.write(line)
                        
#----- Generer une analyse avec ChatGPT                   
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant that analyzes SMART data and define if a disk is ok or not. I dont want any more explanation, just give me a score and a 12 words comment maximum. The score is given from 1 to 10 (1 is the more risky 10 is perfect health), is the disk safe or not. If there is the word "error" at the end of the smart report, please ignore it and dont talk about it.  Before giving the score, print Score = '},
                {'role': 'user', 'content': f'Here is the SMART data for my disk:\n{log_content}'}
            ]
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + api_key
        }

        response = requests.post(url, json=data, headers=headers)
        result = response.json()

        summary = result['choices'][0]['message']['content']
        with open("rapport.txt", "a") as f:
            f.write(summary)
            
# ----- Montrer la progression dans la sortie terminal
        print("Analyse terminée de " + str(count) + " disques")
        count = count + 1


analyze_smart_data()

    
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email.encoders as encoders


# ----- Fonction pour envoyer le fichier de rapport par Email -------

def send_email():
    # Sender and recipient email addresses
    sender_email = SMTP_USER
    recipient_email = EMAIL_RECEIVER
    
    # Subject and body of the email
    subject = "Rapport d'analyses IA des données SMART"
    body = "Voici le fichier rapport.txt en pièce jointe."
    
    # Create a multipart message object
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email
    
    # Attach the body of the email
    message.attach(MIMEText(body))
    
    # Attach the report file
    with open("rapport.txt", "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=rapport.txt",
        )
        message.attach(part)
    
    # Connect to the SMTP server and send the email
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(sender_email, recipient_email, message.as_string())
    

print("Envoi du mail... à "+EMAIL_RECEIVER)
send_email()
print("Mail envoyé.")


