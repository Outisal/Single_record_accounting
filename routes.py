from app import app
import users
import records
from flask import render_template, request, redirect
from datetime import timedelta


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
        business_name = request.form["business_name"]
        business_id = request.form["business_id"]
        if password1 != password2:
            return render_template("error.html", message="passwords don't match")
        if users.register(username, password1, business_name, business_id):
            return redirect("/")
        else:   
            return render_template("error.html", message="Registeration failed.")
        
@app.route("/update_account_data",methods=["GET","POST"])
def maintain_account():
    if request.method == "GET":
        account_data = users.get_account_data()
        return render_template("update_account_data.html", a = account_data)
    if request.method == "POST":
        user_id = request.form["user_id"]
        business_name = request.form["business_name"]
        business_id = request.form["business_id"]
        if len(business_name) > 100:
            return render_template("error.html", message="Business name is too long")   
        if len(business_id) > 100:
            return render_template("error.html", message="Business id is too long")
        users.update_account_data(user_id, business_name, business_id)
        return redirect("/") 
        
@app.route("/update_favorites", methods=["GET","POST"])
def favorites():
    if request.method == "GET":
        favorites = users.get_favorites()
        return render_template("update_favorites.html", f = favorites)
    if request.method == "POST":
        user_id = request.form["user_id"]
        iban = request.form["iban"]
        payment_term = request.form["payment_term"] if request.form["payment_term"] else None
        email = request.form["email"]
        mobile_nr = request.form["mobile_nr"]
        post_address =request.form["post_address"]
        if len(iban) > 34:
            return render_template("error.html", message="IBAN is too long")
        if float(payment_term) > 300:
            return render_template("error.html", message="Payment term should be less than 300 days")         
        if len(email) > 320:
            return render_template("error.html", message="Email is too long") 
        if len(mobile_nr) > 15:
            return render_template("error.html", message="Mobile number is too long") 
        if len(post_address) > 100:
            return render_template("error.html", message="Post address is too long")   
        users.update_favorites(user_id, iban, payment_term, email, mobile_nr, post_address)
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
        amount = request.form["amount"]
        price = request.form["price"]
        if len(title) > 100:
            return render_template("error.html", message="Title is too long")
        if float(price) > 200000:
            return render_template("error.html", message="Price is too high")
        records.add_record(user_id, record_date, title, record_class_id, amount, price)
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
        if len(title) > 100:
            return render_template("error.html", message="Title is too long")
        if float(amount) > 1000:
            return render_template("error.html", message="Amount is too high")
        if float(price) > 200000:
            return render_template("error.html", message="Price is too high")
        if len(iban) > 34:
            return render_template("error.html", message="IBAN is too long")
        if float(payment_term) > 300:
            return render_template("error.html", message="Payment term should be less than 300 days")       
        if len(customer) > 100:
            return render_template("error.html", message="Customer name is too long")    
        if len(email) > 320:
            return render_template("error.html", message="Email is too long") 
        if len(mobile_nr) > 15:
            return render_template("error.html", message="Mobile number is too long") 
        if len(post_address) > 100:
            return render_template("error.html", message="Post address is too long")     
        record_id = records.add_record(user_id, record_date, title, record_class_id, amount, price)
        records.add_invoice(record_id, customer, payment_term, iban, email, mobile_nr, post_address)
        return redirect("/")
    
@app.route("/records")
def view_records():
    record_data = records.show_records()
    return render_template("records.html", value = record_data)

@app.route("/invoice/<int:id>")
def invoice(id):
    i_data = records.get_invoice_data(id)
    due_date = i_data.date + timedelta(days=i_data.payment_term)
    total_wo_vat = round(i_data.price * i_data.amount,2)
    vat_price = round(0.01 * i_data.vat * total_wo_vat,2)
    total = vat_price + total_wo_vat
    return render_template("invoice.html", i = i_data, due_date = due_date, vat_price = vat_price, 
                           total = total, total_wo_vat = total_wo_vat)