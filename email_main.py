from imaplib import IMAP4
from email.message import EmailMessage
from email.parser import Parser
from email.mime.text import MIMEText
from typing import List, Dict
import ssl
import os
import smtplib
import yagmail
from dataclasses import dataclass

import click
import inquirer


@dataclass
class Mails:
    sender: str
    receiver : str
    subject: str
    body: str
    password: str



def sender_receiver_info() -> List[Mails]:
    information_list = []
    while True:
        questions = [
            inquirer.Text('sender', message="Write the email of a sender"),
            inquirer.Text('receiver', message="Write the email of a receiver"),
            inquirer.Text('subject', message="Write the subject"),
            inquirer.Text('body', message="Write the body"),
            inquirer.Text('password', message="Write the password"),
            
        ]
        answer = inquirer.prompt(questions)
        
        try:
            information_list.append(Mails(answer['sender'], answer['receiver'], answer['subject'], answer['body'], answer['password']))
     
        except ValueError:
            print("Invalid input, please enter sender, receiver, subject and body.")
        
        next_information = input('Do you want to add another cost? (y/n): '
                                 ).lower()
        
        if next_information != 'y':
            break
    
    return information_list

 

def send_message(info):
   yag = yagmail.SMTP(info.sender, info.password)
   contents = [info.body]
   yag.send(info.receiver, info.subject, contents)
   # https://github.com/kootenpv/yagmail/blob/master/README.md < - how to work on it

@click.group()
def cli():
    pass  

@cli.command()
def send_email():
    obtaining_informations_list = sender_receiver_info()    # mailparser.parse_from_string(message) < - do parsowania informacji
    
    for info in obtaining_informations_list:
        send_message(info)



if __name__ == '__main__':
    cli()
