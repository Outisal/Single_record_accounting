from db import db
from users import get_logged_in_user_id
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def add_expense(user_id, record_date, title, record_class, price):
    record_type = "Expense"
    amount = 1
    sql = text("""INSERT INTO records (user_id, record_date, title, record_type, record_class, amount, price)
               VALUES(:user_id,:record_date,:title,:record_type,:record_class,:amount,:price)""")
    db.session.execute(sql, {"user_id":user_id, "record_date":record_date, "title":title, "record_type":record_type, 
                             "record_class":record_class, "amount":amount, "price":price})
    db.session.commit()

def add_income(user_id, record_date, title, record_class, amount, price):
    record_type = "Income"
    sql = text("""INSERT INTO records (user_id, record_date, title, record_type, record_class, amount, price)
               VALUES(:user_id,:record_date,:title,:record_type,:record_class,:amount,:price)
               RETURNING id""")
    result = db.session.execute(sql, {"user_id":user_id, "record_date":record_date, "title":title, "record_type":record_type, 
                             "record_class":record_class, "amount":amount, "price":price})
    record_id = result.fetchone()[0]
    db.session.commit()
    return record_id

def add_invoice(record_id, customer, payment_term, vat, iban, email, mobile_nr, post_address):
    sql = text("""INSERT INTO invoice (record_id, customer, payment_term, vat, iban, email, mobile_nr, post_address) 
               VALUES(:record_id,:customer,:payment_term,:vat,:iban,:email,:mobile_nr,:post_address)""")
    db.session.execute(sql, {"record_id":record_id, "customer":customer, "payment_term":payment_term, "vat":vat, 
                             "iban":iban, "email":email, "mobile_nr":mobile_nr, "post_address":post_address})
    db.session.commit()

def show_records():
    user_id = get_logged_in_user_id()
    sql = text("""SELECT R.record_date, R.title, I.id, R.record_type, R.record_class, R.amount * R.price 
               FROM records R LEFT JOIN invoice I ON I.record_id = R.id 
               WHERE R.user_id=:user_id""")
    records_data = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return records_data