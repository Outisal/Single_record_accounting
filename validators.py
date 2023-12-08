import re
from flask import session, abort

def check_csrf(csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)

def check_business_id(business_id):
    #check the format of the business_id
    if len(business_id) > 9:
        return False
    if not business_id[:7].isdigit():
        return False
    if not business_id[8].isdigit():
        return False
    if business_id[7] != "-":
        return False

    factor = [7, 9, 10, 5, 8, 4, 2] # define the factors for business id check digit calculation
    check_sum = 0
    for i in range(7):
        check_sum += int(business_id[i]) * factor[i]
    check_reminder = check_sum % 11
    if check_reminder == 1: #if reminder is 1, business id is not valid
        check_digit = -1
    if check_reminder == 0 and int(business_id[8]) != 0: #if reminder is 0, check digit is 0
        check_digit = 0
    if 2 <= check_reminder <= 10: #if reminder is between 2-10, check digit is 11 - reminder
        check_digit = 11 - check_reminder
    if int(business_id[8]) != check_digit:
        return False
    return True

def check_iban(iban):
    iban = "".join(iban.split())

    #check the format of the iban number
    if len(iban) != 18:
        return False

    #check the format of the country code
    country_code = iban[:2]
    if not country_code.isalpha() or not country_code.isupper():
        return False

    if not iban[2:].isdigit():
        return False

    #calculate if iban number is valid
    country_code_nr = ""
    for char in country_code:
        country_code_nr += str(ord(char) - 55)

    check_number = int(iban[4:] + country_code_nr + iban[2:4]) % 97
    if check_number != 1:
        return False
    return True

def check_email(email):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.match(pattern, email):
        return True
    return False

def check_mobile_nr(mobile_nr):
    mobile_nr = "".join(mobile_nr.split())
    if mobile_nr[0] == "+":
        mobile_nr = mobile_nr[1:]
    if len(mobile_nr) < 5 or len(mobile_nr) > 12:
        return False
    if not mobile_nr.isdigit():
        return False
    return True
