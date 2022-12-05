# Utilities Automator  

## Use 
This is made for my landlord so he can,
* Get all the utilities cost in one place.
* Save the data to a csv file. 
* Email the utilities + rent to all of the renters.

## Set Up 

To install you need to make a .env file with 

```
EMAIL_PASSWORD= 'application password to your gmail'
UTIL_EMAIL= 'email used to log in to your account'
UTIL_PASSWORD= 'password to your account'
ACCOUNT_NUMBER= 'account number'
```

Further more you need to add the right chrome drive to the file.

dependency's 
* selenium 
* beautiful soup
* dotenv
* smtplib

Then to run simply run main.py

