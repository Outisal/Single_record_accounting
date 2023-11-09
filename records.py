from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def add_cost(user_id, record_date, title, record_class, price):
    record_type = "cost"
    amount = 1
    sql = text("""INSERT INTO records (user_id, record_date, title, record_type, record_class, amount, price)
               VALUES(:user_id,:record_date,:title,:record_type,:record_class,:amount,:price)""")
    db.session.execute(sql, {"user_id":user_id, "record_date":record_date, "title":title, "record_type":record_type, 
                             "record_class":record_class, "amount":amount, "price":price})
    db.session.commit()
