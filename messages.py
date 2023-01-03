from datetime import date

def get_message(renter, gas, electricity, internet, upstairs_fraction, downstairs_fraction):
    today = date.today()
    fraction = 0
    if renter.upstairs:
        fraction = upstairs_fraction
    else: 
        fraction = downstairs_fraction

    subject = str(today.strftime("%B")) + ' rent is $' + str(renter.total)
    message = ''
    match today.strftime('%B'):
        case 'January': message = f'''Subject: {subject}\n\nHey {renter.name},
            \nHope you had a great New Year and holiday break!'''
        case 'February': message = f'''Subject: {subject}\n\nHey {renter.name},
            \nOne more month till spring!'''
        case 'September':
            pass
        case 'October': message = f'''Subject: {subject}\n\nHey {renter.name},
            '''
        case 'November': message = f'''Subject: {subject}\n\nHey {renter.name},
            \nHope you had a great Remembrance day weekend!'''
        case 'December': message = f'''Subject: {subject}\n\nHey {renter.name},
            \nMerry Christmas!'''

    message += f''' Just wanted to share the utilities breakdown for last month:

    Gas: {int(fraction * gas)} 
    Electricity: {int(fraction * electricity)}
    Internet: {int(fraction * internet)}
    Total: {int(fraction * (gas + internet + electricity))} 
    
So, total rent is {int(renter.total)} for {str(today.strftime('%B'))}.

Let me know if you have any questions.

Cheers, 
Don'''
    return message

# Base Rent: {int(renter.rent)} # Returns base rent
# Total Utilities: {int(renter.utils_total)}
# So total payable is {int(renter.total)}. Please etransfer the amount to don2xu@gmail.com. 