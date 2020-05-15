import random
import json
import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from tokenz import password

def generate_pass():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    
    password = random.sample(chars, 8)
    password[random.randint(0,7)] = str(random.randint(0,9))
    return ''.join(password)

def create_mail_pass_list():
    mail_data = []
    with open('mails.txt') as f:
        for line in f:
            user_data = {}
            line = line.strip()
            user_data['email'] = line
            user_data['password'] = generate_pass()
            mail_data.append(user_data)
    with open('mail_data.json', 'w') as f:
        json.dump(mail_data, f, indent=4)
    return mail_data

def send_email():
    with open('mail_data.json') as f:
        mail_data = json.load(f)
    server = smtplib.SMTP('mail.stardustpaints.ru', port=587)
    server.starttls()

    server.login('dmitrievs@stardustpaints.ru', password)

    for user_data in mail_data:
        mail_to = user_data['email']
        message = f'Добрый день! В понедельник 18-05-2020 произойдет смена пароля от вашего почтового ящика. Новый пароль {user_data["password"]}'
        message = MIMEText(message, 'plain', 'utf-8')
        message['Subject'] = Header("Смена пароля", 'utf-8')
        message['From'] = "dmitrievs@stardustpaints.ru"
        message['To'] = mail_to
        
        try:
            server.sendmail('dmitrievs@stardustpaints.ru', mail_to, message.as_string())
            print(f'Письмо на ящик {mail_to} отправлено ')
        except:
            print(f'Письмо на ящик {mail_to} отправить не удалось')


if __name__ == "__main__":
    #create_mail_pass_list()
    send_email()

