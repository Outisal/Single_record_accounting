from db import db
from users import get_logged_in_user_id
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def add_record(user_id, record_date, title, record_class_id, amount, price):
    record_class_data = record_type_and_class(record_class_id)
    record_type = record_class_data[0]
    record_class = record_class_data[1]
    vat = record_class_data[2]
    sql = text("""INSERT INTO records (user_id, record_date, title, record_type, record_class, vat, amount, price)
               VALUES(:user_id,:record_date,:title,:record_type,:record_class,:vat,:amount,:price)
               RETURNING id""")
    result = db.session.execute(sql, {"user_id":user_id, "record_date":record_date, "title":title, "record_type":record_type, 
                             "record_class":record_class, "vat":vat, "amount":amount, "price":price})
    record_id = result.fetchone()[0]
    db.session.commit()
    if record_type == 2:
        return record_id

def add_invoice(record_id, customer, payment_term, iban, email, mobile_nr, post_address):
    sql = text("""INSERT INTO invoice (record_id, customer, payment_term, iban, email, mobile_nr, post_address) 
               VALUES(:record_id,:customer,:payment_term,:iban,:email,:mobile_nr,:post_address)""")
    db.session.execute(sql, {"record_id":record_id, "customer":customer, "payment_term":payment_term, 
                             "iban":iban, "email":email, "mobile_nr":mobile_nr, "post_address":post_address})
    db.session.commit()

def show_records():
    user_id = get_logged_in_user_id()
    sql = text("""SELECT R.record_date, R.title, I.id, R.record_type, R.record_class, 
               R.amount * R.price, R.vat, R.vat *0.01 * R.amount * R.price
               FROM records R LEFT JOIN invoice I ON I.record_id = R.id 
               WHERE R.user_id=:user_id""")
    records_data = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return records_data

def get_record_classes(record_type):
    sql = text("""SELECT id, record_class FROM record_class WHERE record_type=:record_type""")
    classes = db.session.execute(sql, {"record_type":record_type}).fetchall()
    return classes

def record_type_and_class(id):
    sql = text("""SELECT record_type, record_class, vat FROM record_class WHERE id=:id""")
    result = db.session.execute(sql, {"id":id}).fetchone()
    return result 

def get_invoice_data(id):
    sql = text("""SELECT I.id id, I.customer customer, I.iban iban, I.email email, 
               I.post_address post_address, I.mobile_nr mobile_nr, I.payment_term payment_term,
               R.title title, R.vat vat, R.amount amount, R.price price, R.record_date date,
               U.business_name business_name, U.business_id business_id
               FROM invoice I LEFT JOIN records R ON I.record_id = R.id 
               LEFT JOIN users U ON R.user_id = U.id
               WHERE I.id=:id""")
    invoice_data = db.session.execute(sql, {"id":id}).fetchone()
    return invoice_data