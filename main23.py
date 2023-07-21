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

gas = get_gas()
electricity = get_electricity()
internet = 45
utils_total = internet + gas + electricity
upstairs_fraction =  0.25
downstairs_fraction = 0.25
email_password  = os.getenv("EMAIL_PASSWORD")

def main():
    global gas, electricity, internet, utils_total
    # Varibles to be used later
   
    today = date.today()
    renters = [#upstairs_a := Renter(os.getenv("58_UPSTAIR_AEMAIL"), 1300, os.getenv("58_UPSTAIR_A"), True),
               #upstairs_b := Renter(os.getenv("58_UPSTAIR_BEMAIL"), 1300, os.getenv("58_UPSTAIR_B"), True),
               downstairs_a := Renter(os.getenv("23_DOWNSTAIRS_AEMAIL"), 1350, os.getenv("23_DOWNSTAIRS_A"), True),
               downstairs_b := Renter(os.getenv("23_DOWNSTAIRS_AEMAIL"), 1300, os.getenv("23_DOWNSTAIRS_B"), True),
               master := Renter(os.getenv("58_UPSTAIR_MSTREMAIL"), 1500, os.getenv("58_UPSTAIR_MSTR"), True)
              ]
              
    # This will add an entry to bills.csv
    exl_write([[
	    today.strftime("%B %d %Y"),
	    gas, 
        electricity,
        internet,
	    utils_total,
	    #upstairs_a.total, 
	    #upstairs_b.total,
	    downstairs_a.total,
	    downstairs_b.total,
        #master.total
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


def email(message):
    global email_password 
    user = os.getenv("EMAIL_ADDRESS")
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(user, email_password)
        smtp_server.send_message(message)
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

