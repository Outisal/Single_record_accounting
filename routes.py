from app import app
import users
import records
from flask import render_template, request, redirect


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Incorrect username or password")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="passwords don't match")
        if users.register(username, password1):
            return redirect("/")
        else:   
            return render_template("error.html", message="Registeration failed")
        
@app.route("/update_favorites", methods=["GET","POST"])
def favorites():
    if request.method == "GET":
        favorites = users.get_favorites()
        if favorites:
            return render_template("update_favorites.html", business_id = favorites.business_id, iban = favorites.iban, 
                                   payment_term = favorites.payment_term, email = favorites.email, 
                                   mobile_nr = favorites.mobile_nr, post_address = favorites.post_address)
        return render_template("update_favorites.html")
    if request.method == "POST":
        user_id = request.form["user_id"]
        business_id = request.form["business_id"]
        iban = request.form["iban"]
        payment_term = request.form["payment_term"] if request.form["payment_term"] else None
        email = request.form["email"]
        mobile_nr = request.form["mobile_nr"]
        post_address =request.form["post_address"]
        users.update_favorites(user_id, business_id, iban, payment_term, email, mobile_nr, post_address)
        return redirect("/")
    
@app.route("/add_expense", methods=["GET","POST"])
def add_expense():
    if request.method == "GET":
        classes = records.get_record_classes("Expense")
        return render_template("add_expense.html", classes = classes)
    if request.method == "POST":
        user_id = request.form["user_id"]
        record_date = request.form["record_date"]
        title = request.form["title"]
        record_class_id = request.form["record_class"]
        price = request.form["price"]
        records.add_expense(user_id, record_date, title, record_class_id, price)
        return redirect("/")
    
@app.route("/add_income", methods=["GET","POST"])
def add_income():
    if request.method == "GET":
        favorites = users.get_favorites()
        classes = records.get_record_classes("Income")
        if favorites:
            return render_template("add_income.html", classes = classes, iban = favorites.iban, payment_term = favorites.payment_term, 
                               email = favorites.email, mobile_nr = favorites.mobile_nr, post_address = favorites.post_address)
        else:
            return render_template("add_income.html", classes = classes)
    if request.method == "POST":
        user_id = request.form["user_id"]
        record_date = request.form["record_date"]
        record_class_id = request.form["record_class"]
        amount = request.form["amount"]
        price = request.form["price"]
        payment_term = request.form["payment_term"]
        customer = request.form["customer"]
        title = request.form["title"]
        iban = request.form["iban"]
        email = request.form["email"]
        mobile_nr = request.form["mobile_nr"]
        post_address =request.form["post_address"]
        record_id = records.add_income(user_id, record_date, title, record_class_id, amount, price)
        records.add_invoice(record_id, customer, payment_term, iban, email, mobile_nr, post_address)
        return redirect("/")
    
@app.route("/records")
def view_records():
    record_data = records.show_records()
    return render_template("records.html", value = record_data)