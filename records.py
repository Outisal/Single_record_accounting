from sqlalchemy.sql import text
from db import db
from users import get_logged_in_user_id

class Record:
    def __init__(self):
        pass

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def record_id(self):
        return self.__record_id

    @record_id.setter
    def record_id(self, record_id):
        self.__record_id = record_id

    @property
    def record_date(self):
        return self.__record_date

    @record_date.setter
    def record_date(self, record_date):
        self.__record_date = record_date

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def record_class(self):
        return self.__record_class

    @record_class.setter
    def record_class(self, record_class_id):
        record_class_data = record_type_and_class(record_class_id)
        self.__record_class = record_class_data[1]
        self.__record_type = record_class_data[0]
        self.__vat = record_class_data[2]

    @property
    def record_type(self):
        return self.__record_type

    @record_type.setter
    def record_type(self, record_type):
        self.__record_type = record_type

    @property
    def vat(self):
        return self.__vat

    @vat.setter
    def vat(self, vat):
        self.__vat = vat

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, amount):
        self.__amount = amount

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

class Invoice:

    def __init__(self) -> None:
        pass

    @property
    def record_id(self):
        return self.__record_id

    @record_id.setter
    def record_id(self, record_id):
        self.__record_id = record_id

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, customer):
        self.__customer = customer

    @property
    def iban(self):
        return self.__iban

    @iban.setter
    def iban(self, iban):
        self.__iban = iban

    @property
    def payment_term(self):
        return self.__payment_term

    @payment_term.setter
    def payment_term(self, payment_term):
        self.__payment_term = payment_term

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def mobile_nr(self):
        return self.__mobile_nr

    @mobile_nr.setter
    def mobile_nr(self, mobile_nr):
        self.__mobile_nr = mobile_nr

    @property
    def post_address(self):
        return self.__post_address

    @post_address.setter
    def post_address(self, post_address):
        self.__post_address = post_address

def add_record(record):
    sql = text("""INSERT INTO records (user_id, record_date, title,
               record_type, record_class, vat, amount, price)
               VALUES(:user_id,:record_date,:title,:record_type,:record_class,:vat,:amount,:price)
               RETURNING id""")
    result = db.session.execute(sql, {"user_id":record.user_id, "record_date":record.record_date,
                                      "title":record.title, "record_type":record.record_type,
                                      "record_class":record.record_class, "vat":record.vat,
                                      "amount":record.amount, "price":record.price})
    record_id = result.fetchone()[0]
    db.session.commit()
    return record_id

def add_invoice(invoice):
    sql = text("""INSERT INTO invoice (record_id, customer, payment_term,
               iban, email, mobile_nr, post_address)
               VALUES(:record_id,:customer,:payment_term,:iban,:email,:mobile_nr,:post_address)""")
    db.session.execute(sql, {"record_id":invoice.record_id, "customer":invoice.customer,
                             "payment_term":invoice.payment_term, "iban":invoice.iban,
                             "email":invoice.email, "mobile_nr":invoice.mobile_nr,
                             "post_address":invoice.post_address})
    db.session.commit()

def show_records():
    user_id = get_logged_in_user_id()
    sql = text("""SELECT R.record_date, R.title, I.id, R.record_type, R.record_class,
               R.amount * R.price, R.vat, R.vat * 0.01 * R.amount * R.price, R.id
               FROM records R LEFT JOIN invoice I ON I.record_id = R.id 
               WHERE R.user_id=:user_id ORDER BY R.record_date DESC""")
    records_data = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return records_data

def get_record_classes(record_type):
    sql = text("""SELECT id, record_class FROM record_class WHERE record_type=:record_type""")
    classes = db.session.execute(sql, {"record_type":record_type}).fetchall()
    return classes

def record_type_and_class(record_id):
    sql = text("""SELECT record_type, record_class, vat FROM record_class WHERE id=:id""")
    result = db.session.execute(sql, {"id":record_id}).fetchone()
    return result

def get_invoice_id(record_id):
    sql = text("""SELECT I.id FROM invoice I
               LEFT JOIN records R ON I.record_id = R.id
               WHERE I.record_id=:record_id""")
    invoice_id = db.session.execute(sql, {"record_id":record_id}).fetchone()
    return invoice_id[0]

def get_invoice_data(invoice_id):
    sql = text("""SELECT I.id id, I.customer customer, I.iban iban, I.email email,
               I.post_address post_address, I.mobile_nr mobile_nr, I.payment_term payment_term,
               R.title title, R.vat vat, R.amount amount, R.price price, R.record_date date,
               U.business_name business_name, U.business_id business_id, R.record_class record_class
               FROM invoice I LEFT JOIN records R ON I.record_id = R.id
               LEFT JOIN users U ON R.user_id = U.id
               WHERE I.id=:invoice_id""")
    invoice_data = db.session.execute(sql, {"invoice_id":invoice_id}).fetchone()
    return invoice_data

def get_record_data(record_id):
    sql = text("""SELECT id, record_date, title, record_type, record_class, vat, amount, price
               FROM records WHERE id=:record_id""")
    record_data = db.session.execute(sql, {"record_id":record_id}).fetchone()
    return record_data

def remove_record_data(record_id, record_type):
    if record_type == 2:
        sql = text("""DELETE FROM invoice WHERE record_id=:id""")
        db.session.execute(sql, {"id":record_id})
    sql = text("""DELETE FROM records WHERE id=:id""")
    db.session.execute(sql, {"id":record_id})
    db.session.commit()

def update_record_data(record):
    sql = text("""UPDATE records SET record_date=:record_date, title=:title,
               record_class=:record_class, vat=:vat, amount=:amount, price=:price 
               WHERE id=:id""")
    db.session.execute(sql,{"record_date":record.record_date, "title":record.title,
                            "record_class":record.record_class, "vat":record.vat,
                            "amount":record.amount, "price":record.price, "id":record.record_id})
    db.session.commit()

def update_invoice(invoice):
    sql = text("""UPDATE invoice SET customer=:customer, payment_term=:payment_term,
               iban=:iban, email=:email, mobile_nr=:mobile_nr, 
               post_address=:post_address WHERE record_id=:record_id""")
    db.session.execute(sql,{"customer":invoice.customer, "payment_term":invoice.payment_term,
                            "iban":invoice.iban,"email":invoice.email,"mobile_nr":invoice.mobile_nr,
                            "post_address":invoice.post_address, "record_id":invoice.record_id})
    db.session.commit()
