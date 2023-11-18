from sqlalchemy.sql import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

class Favorites:

    def __init__(self) -> None:
        pass

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

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

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["username"] = username
        session["user_id"] = user.id
        return True
    return False

def logout():
    del session["username"]

def register(username, password, business_name, business_id):
    hash_value = generate_password_hash(password)
    try:
        sql = text("""INSERT INTO users (username,password,business_name,business_id)
                   VALUES (:username,:password,:business_name,:business_id)""")
        db.session.execute(sql, {"username":username, "password":hash_value,
                                 "business_name":business_name, "business_id":business_id})
        db.session.commit()
    except:
        return False
    return login(username, password)

def get_account_data():
    user_id = get_logged_in_user_id()
    sql = text("SELECT business_name, business_id FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()

def update_account_data(user_id, business_name, business_id):
    sql = text("""UPDATE users SET business_name=:business_name, business_id=:business_id
                   WHERE id=:user_id""")
    db.session.execute(sql,{"user_id":user_id, "business_name":business_name,
                            "business_id":business_id})
    db.session.commit()

def get_favorites():
    user_id = get_logged_in_user_id()
    sql = text("""SELECT iban, payment_term, email, mobile_nr,
               post_address FROM favorites WHERE user_id=:user_id""")
    favorites = db.session.execute(sql, {"user_id":user_id}).fetchone()
    return favorites


def update_favorites(favorites):
    sql = text("SELECT user_id FROM favorites WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":favorites.user_id})
    user = result.fetchone()
    if user:
        sql = text("""UPDATE favorites SET iban=:iban, payment_term=:payment_term,
                   email=:email, mobile_nr=:mobile_nr, post_address=:post_address
                   WHERE user_id=:user_id""")
        db.session.execute(sql,{"user_id":favorites.user_id, "iban":favorites.iban,
                                "payment_term":favorites.payment_term, "email":favorites.email,
                                "mobile_nr":favorites.mobile_nr,
                                "post_address":favorites.post_address})
        db.session.commit()
    else:
        sql = text("""INSERT INTO favorites (user_id, iban, payment_term, email,
                   mobile_nr, post_address)
                   VALUES (:user_id,:iban,:payment_term,:email,:mobile_nr,:post_address)""")
        db.session.execute(sql,{"user_id":favorites.user_id, "iban":favorites.iban,
                                "payment_term":favorites.payment_term, "email":favorites.email,
                                "mobile_nr":favorites.mobile_nr,
                                "post_address":favorites.post_address})
        db.session.commit()

def get_logged_in_user_id():
    return session.get("user_id",0)
