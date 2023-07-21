from datetime import date
from email.message import EmailMessage

def get_message(renter, gas, electricity, internet, upstairs_fraction, downstairs_fraction):
    today = date.today()
    fraction = 0
    if renter.upstairs:
        fraction = upstairs_fraction
    else: 
        fraction = downstairs_fraction

    subject = str(today.strftime("%B")) + ' rent is $' + str(renter.total)
    message = EmailMessage()
    message['To']=renter.email
    match today.strftime('%B'):
        case 'September':
            pass
        case 'October': message = f'''Subject: {subject}\n\nHey {renter.name},
            '''
        case 'November': message = f'''Subject: {subject}\n\nHey {renter.name},
            \nHope you had a great Remembrance day weekend!'''
        case 'December': message = f'''Subject: {subject}\n\nHey {renter.name},
            \nMerry Christmas!
            '''
    message['Subject']=subject

    message.set_content(f'''\n\n
  <html>
    <head></head>
    <body>
        <p>Just wanted to share the utilities breakdown for last month.</p>
                        

    <p>Gas: {int(fraction * gas)} </p>
    <p>Electricity: {int(fraction * electricity)}</p>
    <p>Internet: {int(fraction * internet)}</p>
    <p>Total: {int(fraction * (gas + internet + electricity))} </p>
    
    <p>So total payable is {int(renter.total)}. Please etransfer the amount to don2xu@gmail.com</p>

    <p>Let me know if you have any questions.</p>

    <p>Cheers, </p>
    <p>Don</p>
  </body>
</html>''')
    return message

# Base Rent: {int(renter.rent)} # Returns base rent
# Total Utilities: {int(renter.utils_total)}
# So total payable is {int(renter.total)}. Please etransfer the amount to don2xu@gmail.com. 