import os
import datetime
import openai
import smtplib
import sys
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email.encoders as encoders
import requests
import csv
import configparser


# --- Import des variables depuis le fichier config.ini ---
config = configparser.ConfigParser()
config.read('config.ini')

# ------- Configuration SMTP -------
SMTP_SERVER = config['settings']['SMTP_SERVER']
SMTP_PORT = int(config['settings']['SMTP_PORT'])
SMTP_USER = config['settings']['SMTP_USER']
SMTP_PASSWORD = config['settings']['SMTP_PASSWORD']
EMAIL_RECEIVER = config['settings']['EMAIL_RECEIVER']

# ------- Configuration OpenAI -------
openai.api_key = config['settings']['openai.api_key']
PROMPT = config['settings']['PROMPT']
PROMPT_GPT4 = config['settings']['PROMPT_GPT4']


# ------- Configuration du dossier des logs -------
LOG_DIR = "./logs/"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
filename = "table.csv"
disk_name = None

def clear_stdout():
    sys.stdout.flush()
    sys.stdout.write("\033[F")  # Move cursor up one line
    sys.stdout.write("\033[K")  # Clear current line

def total_clear_stdout():
    import os
    os.system('clear')
    
def extract_smart_logs():
    import subprocess
    import os
    import glob
    
    os.makedirs(LOG_DIR, exist_ok=True)
    file_list = glob.glob(f"{LOG_DIR}/*.txt")
    for file in file_list:
        os.remove(file)
    
    disks = subprocess.check_output("smartctl --scan | grep scsi", shell=True).decode().splitlines()
    count = 1
    for disk in disks:
        print("Extracting SMART reports... "+str(count)+" reports created" )
        clear_stdout()
        count=count+1
        disk_name = disk.split()[0]
        log_file = os.path.join(LOG_DIR, f"smart_logs_{disk_name.replace('/', '_')}.txt")
        os.system(f"smartctl --all {disk_name} | head -n 13 | tail -n 9 >> {log_file}")
        log_file = os.path.join(LOG_DIR, f"smart_logs_{disk_name.replace('/', '_')}.txt")
        os.system(f"smartctl --all {disk_name} | head -n 86 | tail -n 27 | awk '{{print $2,$4,$5,$6,$10}}' | column -t -s ' ' >> {log_file}")
    
    print("SMART report extraction completed, "+str(count)+" reports created." )
    
def analyze_smart_data():
    if os.path.exists("table.csv"):
        os.remove("table.csv")
    count = 1
    
    log_files = sorted(os.listdir(LOG_DIR))
    for log_file in log_files:
        if log_file.endswith('.txt'):
            with open(os.path.join(LOG_DIR, log_file), 'r') as f:
                log_content = f.read()
                print('analysing : ' + log_file)
                
        # Remplacez 'YOUR_API_KEY' par votre clé d'API GPT-3
        api_key = openai.api_key
        url = 'https://api.openai.com/v1/chat/completions'
        
        with open("rapport.txt", "a") as f:
            f.write("\n\n")
            f.write("- - - - - - - - - - - - - - ")
            f.write("\n\n")
        
        
        file_name = os.path.splitext(os.path.basename(log_file))[0]
        last_underscore_index = file_name.rfind('_')
        characters_after_last_underscore = file_name[last_underscore_index + 1:]
        
        with open("rapport.txt", "a") as f:
            f.write("Disk : " + characters_after_last_underscore)
            f.write("\n")
        

        log_file_path = os.path.join(LOG_DIR, log_file)
        with open(log_file_path, 'r') as f:
            import re
            for line in f:
                if re.match(r"(Serial Number)", line):
                    serial = line.split(":")[1].strip()
                            
                    
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': PROMPT},
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
            

        csv_file = "table.csv"
        csv_exists = os.path.isfile(csv_file)
        
        score_match = re.search(r"Score=(\d+)", summary)
        score = score_match.group(1) if score_match else ""
    
        summary = summary.replace("Score=", "")
        summary = summary.lstrip("0123456789.")
        summary = summary.replace("\n", "")
        
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if not csv_exists:
                writer.writerow(['Serial','Device','Score', 'IA'])
            writer.writerow([serial, characters_after_last_underscore, score, summary])
                
        print("Analyzing " + str(count) + " disks")
        count = count + 1

        clear_stdout()
        
    print("Analysis completed, "+str(count)+" disks analyzed." )
    
def get_disk_name():
    global disk_name
    disk_name = input("Which disk do you want to analyze? ")
    return disk_name

def analyze_special_disk():
    # Delete the rapport_gpt4.txt file
    os.remove("rapport_gpt4.txt")

    # Add a line with the date, time, and disk name to the rapport_gpt4.txt file
    with open("rapport_gpt4.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - Disk Name: {disk_name}\n")
    
    import subprocess
    log = subprocess.check_output(f"smartctl --all /dev/{disk_name} | head -n 85", shell=True).decode()
    print('Analysis of '+ disk_name +' in progress...' )
  
    global summary         
    api_key = openai.api_key
    url = 'https://api.openai.com/v1/chat/completions'
    
    
    data = {
        'model': 'gpt-4',
        'messages': [
            {'role': 'system', 'content': PROMPT_GPT4},
            {'role': 'user', 'content': f'Here is the SMART data for my disk:\n{log}'}
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }

    response = requests.post(url, json=data, headers=headers)
    result = response.json()

    summary = result.get('choices', [{}])[0].get('message', {}).get('content', '')

    total_clear_stdout()
    print('Analysis of '+ disk_name +' completed' )
    input("Press enter to print the GPT4 analysis for "+ disk_name+'...')

    total_clear_stdout()
    print("Here is the GPT4 report for " + disk_name)
    print()
    print(summary)
    with open("rapport_gpt4.txt", "a") as f:
        f.write("\n")
        f.write(summary)
    print()

def sort_csv(filename):
    
    # Read the CSV file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    # Sort the data by the 'score' column
    sorted_data = sorted(data, key=lambda row: float(row[2]) if row[2].isdigit() else 0)

    # Write the sorted data back to the CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sorted_data)

def csv_to_html(filename):
    if os.path.exists("table.html"):
        os.remove("table.html")
    
    html_content = """
<html>
<head>
<style>
table { border-collapse: collapse; width: 50%; }
th, td { border: 1px solid black; padding: 8px 12px; }
th { background-color: #f2f2f2; }
td.score { background-color: rgb(0, 255, 0); }
td.score-1 { background-color: red; }
td.score-2 { background-color: orange; }
td.score-3 { background-color: yellow; }
td.score-4 { background-color: lightgreen; }
</style>
</head>
<body>
<table>
"""

    with open(filename, 'r') as file:
        reader = csv.reader(file)

        # Headers
        headers = next(reader)
        html_content += "<tr>\n"
        for header in headers:
            html_content += f"<th>{header}</th>\n"
        html_content += "</tr>\n"

        # Rows
        for row in reader:
            html_content += "<tr>\n"
            for col in row:
                score_class = ""
                if col.isdigit():
                    score = int(col)
                    if score == 0:
                        score_class = 'score-1'
                    elif 1 <= score <= 4:
                        score_class = 'score-1'
                    elif 5 <= score <= 6:
                        score_class = 'score-2'
                    elif 7 <= score <= 8:
                        score_class = 'score-3'
                    elif 9 <= score <= 10:
                        score_class = 'score-4'
                    html_content += f"<td class='{score_class}'>{col}</td>\n"
                else:
                    html_content += f"<td>{col}</td>\n"
            html_content += "</tr>\n"

    html_content += "</table>\n</body>\n</html>"

    with open("table.html", 'w') as output_file:
        output_file.write(html_content)

def send_email():
    print("Sending email... to "+EMAIL_RECEIVER)
    # Sender and recipient email addresses
    sender_email = SMTP_USER
    recipient_email = EMAIL_RECEIVER
    
    # Subject and body of the email
    subject = "IA Analysis Report of SMART Data"
    body = "Here is the report file rapport.txt as an attachment."
    
    # Create a multipart message object
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email
    
    # Attach the body of the email
    message.attach(MIMEText(body))
    
    # Attach the report file
    with open("table.html", "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=table.html",
        )
        message.attach(part)
    
    # Connect to the SMTP server and send the email
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(sender_email, recipient_email, message.as_string())
        
    print("Email sent.")
    input("Press enter to continue...")

def send_email_GPT4():
    
    send_report_by_email = input("Do you want to receive the report by email? (y/n) ")
    
    if send_report_by_email.lower() == "y":
        print()
    else:
        main()
    
    print("Sending email... to "+EMAIL_RECEIVER)
    # Sender and recipient email addresses
    sender_email = SMTP_USER
    recipient_email = EMAIL_RECEIVER
    
    # Subject and body of the email
    subject = "IA Analysis Report of SMART Data for disk " + disk_name
    body = "Here is the report file as an attachment."
    
    # Create a multipart message object
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email
    
    # Attach the body of the email
    message.attach(MIMEText(body))
    
    # Attach the report file
    with open("rapport_gpt4.txt", "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=rapport_gpt4.txt",
        )
        message.attach(part)
    
    # Connect to the SMTP server and send the email
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(sender_email, recipient_email, message.as_string())
        
    print("Email sent.")
    input("Press enter to continue...")

def main():
    total_clear_stdout()
    import time

    # ASCII Art for a disk
    ascii_art = [
    "  __________________",
    " |  :           :  |",
    " |  :           :  |",
    " |  DiskIAnalyser  |",
    " |  :   v0.2    :  |",
    " |  :___________:  |",
    " |     _________   |",
    " |    | __      |  |",
    " |    ||  |     |  |",
    " \____||__|_____|__|"
      
    ]

    # Function to display the ASCII art progressively
    def display_ascii_art():
        for line in ascii_art:
            print(line)
            time.sleep(0.1)  # Delay for half a second between lines

    # Testing the function
    display_ascii_art()
    print()
    print("Options:")
    print("1. Analyze SMART data for all disks and receive a report by email")
    print("2. Analyze SMART data for a specific disk (GPT4)")
    print("3. Quit")
    
    choice = input("Please choose an option: ")
    
    if choice == "1":
        total_clear_stdout
        extract_smart_logs()
        analyze_smart_data()
        sort_csv(filename)
        csv_to_html(filename)
        send_email()
        main()
        
    if choice == "2":
        total_clear_stdout()
        get_disk_name()
        analyze_special_disk()
        send_email_GPT4()
        main()
        
    elif choice == "3":
        print("Goodbye!")
        sys.exit()
        
    else:
        print("Invalid option. Please choose a valid option.")
        main()
        
main()