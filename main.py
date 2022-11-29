import csv
import os
import smtplib
from datetime import date
from email.message import EmailMessage

from dotenv import load_dotenv
from openpyxl import load_workbook

from messages import get_message
from web_scrape import get_electricity, get_gas


load_dotenv()

gas = 1 #get_gas()
electricity = 1 #get_electricity()
internet = 45
utils_total = internet + gas + electricity
upstairs_fraction =  0.22
downstairs_fraction = 0.17

email_password  = os.getenv("EMAIL_PASSWORD")

def main():
    global gas, electricity, internet, utils_total
    # Varibles to be used later
   
    today = date.today()
    renters = [upstairs_a := Renter('philyclements@outlook.com', 1300, 'Philip', True),
               upstairs_b := Renter('nicholas.scott.demetrick@gmail.com', 1300, 'Nick', True),
               #downstairs_a := Renter('don2xu@gmail.com', 1350, 'philip', True),
               #downstairs_b := Renter('zmxnfg@gmail.com', 1300, 'nick', True),
               master := Renter('sam.chow24@gmail.com', 1500, 'Shiva', True)
              ]
              
    # This will add an entry to bills.csv
    exl_write([[
	    today.strftime("%B %d %Y"),
	    gas, 
        electricity,
        internet,
	    utils_total,
	    upstairs_a.total, 
	    upstairs_b.total,
	    #downstairs_a.total,
	    #downstairs_b.total,
        master.total
        ]], 
	    'bills.xlsx')
    
    # This will go through all the renters and send an email.
    
    print('Sending emails')
    for renter in renters:
        if input(f'Send email to {renter.name}: ') == 'y':
            message = get_message(renter, gas, electricity, internet,
                                upstairs_fraction, downstairs_fraction)

            email(renter.email, message)
    
    print('done')


class Renter():
    def __init__(self, email, rent, name, upstairs):
        global utils_total, upstairs_fraction, downstairs_fraction

        self.name = name
        self.rent = rent
        self.email = email
        self.upstairs = upstairs
        if upstairs:
            self.total = int(rent + upstairs_fraction * utils_total) 
        else:
            self.total = int(rent + downstairs_fraction * utils_total) 


def email(to, content):
    global email_password 
    user = os.getenv("EMAIL_ADDRESS")
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(user, email_password)
        smtp_server.sendmail(user, to, content)
        smtp_server.close()
        print ("Email sent successfully!")

    except Exception as ex:
        print ("Something went wrong….",ex)

def exl_write(data, file_name):
    file_path = r'C:\Users\don2x\OneDrive - my.yorku.ca\Documents\zHouse\Utilities-Automator' + '\\' + file_name
    wb = load_workbook(file_path)
    ws = wb.worksheets[0]
    for row_data in data:
        ws.append(row_data)
    wb.save(file_path)


def csv_write(data , file_name): 
    for fields in data: 
        with open(file_name, 'a', encoding="utf-8", newline='') as f:
            writer = csv.writer(f) 
            writer.writerow(fields.values()) 
    f.close()

if __name__ == '__main__':
	main()

