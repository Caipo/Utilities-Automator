from web_scrape import get_gas, get_electricity
import csv
from datetime import date
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from dotenv import load_dotenv
import os

load_dotenv()

GAS = get_gas()
electricity = get_electricity()
internet = 75
utils_total = internet + gas + electricity
upstairs_fraction =  0.22
downstairs_fraction = 0.17

email_password  = os.getenv("EMAIL_PASSWORD")

def main():
    global gas, electricity, internet, utils_total
    # Varibles to be used later
   
    today = date.today()
    renters = [upstairs_a := Renter('mr.dino.rex@gmail.com', 1300, 'nick', True),
               upstairs_b := Renter('mr.dino.rex@gmail.com', 1300, 'nick', True),
               downstairs_a := Renter('mr.dino.rex@gmail.com', 1300, 'nick', True),
               downstairs_b := Renter('mr.dino.rex@gmail.com', 1300, 'nick', True),
               masters := Renter('mr.dino.rex@gmail.com', 1300, 'nick', True)
              ]
              
    # This will add an entry to bills.csv
    csv_write([{
	    'Date' : today.strftime("%B %d %Y"),
	    'Gas' : gas, 
        'Electricity' : electricity,
	    'Util Total' : utils_total,
        'Final Total': sum( [i.total for i in renters]) + utils_total,
	    'Upstairs A': upstairs_a.total, 
	    'Upstairs B': upstairs_b.total,
	    'Master' : masters.total,
	    'Downstairs A': downstairs_a.total,
	    'Downstairs B': downstairs_b.total 
	    }], 
	    'bill.csv')
    
    # This will go through all the renters and send an email.
    for i in renters:
        fraction = 0
        if i.upstairs:
            fraction = upstairs_fraction
        else: 
            fraction = downstairs_fraction

        message = f'''
        Your total rent payement for the month of {today.strftime("%B")} is a total of {int(i.rent + fraction * (gas + internet))}. The break down is as follows
        Rent: {int(i.rent)}
        Gas: {int(fraction * gas)} 
        Electricity: {int(fraction * electricity)}
        Internet: {int(fraction * internet)}
        '''
        email(i.email, message)

    print('Done')


class Renter():
    def __init__(self, email, rent, name, upstairs):
        global utils_total

        self.name = name
        self.rent = rent
        self.email = email
        self.upstairs = upstairs
        self.total = rent + utils_total 


def email(to, content):
    global email_password 
    user = 'loansharkdon62@gmail.com'# Email were sending with
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(user, email_password)
        smtp_server.sendmail(user, to, content)
        smtp_server.close()
        print ("Email sent successfully!")

    except Exception as ex:
        print ("Something went wrong….",ex)

def csv_write(data , file_name): 
    for fields in data: 
        with open(file_name, 'a', encoding="utf-8", newline='') as f:
            writer = csv.writer(f) 
            writer.writerow(fields.values()) 
    f.close()

if __name__ == '__main__':
	main()

