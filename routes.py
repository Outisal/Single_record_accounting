from datetime import timedelta
from flask import render_template, request, redirect
from app import app
import users
import records
import validators

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
        if len(username) > 100:
            return render_template("error.html", message="Username is too long")
        if users.username_used(username):
            return render_template("error.html", message="Username is already taken")
        if password1 != password2:
            return render_template("error.html", message="passwords don't match")
        if len(password1) > 100:
            return render_template("error.html", message="Password is too long")
        if len(business_name) > 100:
            return render_template("error.html", message="Business name is too long")
        if not validators.check_business_id(business_id):
            return render_template("error.html", message="""Business id is in wrong format.
                                   Business id should consist of 7 digits,
                                   a hyphen ("-"), and a check digit.""")
        if users.register(username, password1, business_name, business_id):
            return redirect("/")
        return render_template("error.html", message="Registeration failed.")

@app.route("/update_account_data",methods=["GET","POST"])
def maintain_account():
    if request.method == "GET":
        account_data = users.get_account_data()
        return render_template("update_account_data.html", a = account_data)
    if request.method == "POST":
        validators.check_csrf(request.form["csrf_token"])
        user_id = request.form["user_id"]
        business_name = request.form["business_name"]
        business_id = request.form["business_id"]
        if len(business_name) > 100:
            return render_template("error.html", message="Business name is too long.")
        if not validators.check_business_id(business_id):
            return render_template("error.html", message="""Business id is in wrong format.
                                   Business id should consist of 7 digits,
                                   a hyphen ("-"), and a check digit.""")
        users.update_account_data(user_id, business_name, business_id)
        return redirect("/")

@app.route("/update_favorites", methods=["GET","POST"])
def favorites():
    if request.method == "GET":
        favorites_now = users.get_favorites()
        return render_template("update_favorites.html", f = favorites_now)
    if request.method == "POST":
        validators.check_csrf(request.form["csrf_token"])
        new_favorites = users.Favorites
        new_favorites.user_id = request.form["user_id"]
        new_favorites.iban = request.form.get("iban")
        payment_term = request.form["payment_term"] if request.form["payment_term"] else None
        new_favorites.payment_term = payment_term
        new_favorites.email = request.form.get("email")
        new_favorites.mobile_nr = request.form.get("mobile_nr")
        new_favorites.post_address =request.form.get("post_address")
        if not validators.check_iban(new_favorites.iban):
            return render_template("error.html", message="IBAN is invalid")
        if payment_term:
            if float(new_favorites.payment_term) > 300:
                return render_template("error.html",
                                       message="Payment term should be less than 300 days")
        if len(new_favorites.email) > 320:
            return render_template("error.html", message="Email is too long")
        if len(new_favorites.mobile_nr) > 15:
            return render_template("error.html", message="Mobile number is too long")
        if len(new_favorites.post_address) > 100:
            return render_template("error.html", message="Post address is too long")
        users.update_favorites(new_favorites)
        return redirect("/")

@app.route("/add_expense", methods=["GET","POST"])
def add_expense():
    if request.method == "GET":
        classes = records.get_record_classes(1)
        return render_template("add_expense.html", classes = classes)
    if request.method == "POST":
        validators.check_csrf(request.form["csrf_token"])
        expense = records.Record()
        expense.user_id = request.form["user_id"]
        expense.record_date = request.form["record_date"]
        expense.record_class = request.form["record_class"]
        expense.amount = request.form["amount"]
        expense.title = request.form["title"]
        expense.price = request.form["price"]
        if len(expense.title) > 100:
            return render_template("error.html", message="Title is too long")
        if float(expense.price) > 200000:
            return render_template("error.html", message="Price is too high")
        records.add_record(expense)
        return redirect("/records")

@app.route("/update_expense/<int:record_id>", methods=["GET","POST"])
def update_expense(record_id):
    record_data = records.get_record_data(record_id)
    if request.method == "GET":
        classes = records.get_record_classes(1)
        return render_template("update_expense.html", classes = classes, r = record_data)
    if request.method == "POST":
        validators.check_csrf(request.form["csrf_token"])
        expense = records.Record()
        expense.record_id = record_id
        expense.record_date = request.form["record_date"]
        expense.record_class = request.form["record_class"]
        expense.amount = request.form["amount"]
        expense.title = request.form["title"]
        expense.price = request.form["price"]
        if len(expense.title) > 100:
            return render_template("error.html", message="Title is too long")
        if float(expense.price) > 200000:
            return render_template("error.html", message="Price is too high")
        records.update_record_data(expense)
        return redirect("/records")

@app.route("/add_income", methods=["GET","POST"])
def add_income():
    if request.method == "GET":
        favorites_now = users.get_favorites()
        classes = records.get_record_classes(2)
        if favorites_now:
            return render_template("add_income.html", classes = classes, f = favorites_now)
        return render_template("add_income.html", classes = classes)
    if request.method == "POST":
        validators.check_csrf(request.form["csrf_token"])
        income = records.Record()
        invoice_data = records.Invoice()
        income.user_id = request.form["user_id"]
        income.record_date = request.form["record_date"]
        income.record_class = request.form["record_class"]
        income.title = request.form["title"]
        income.amount = request.form["amount"]
        income.price = request.form["price"]
        invoice_data.payment_term = request.form["payment_term"]
        invoice_data.customer = request.form["customer"]
        invoice_data.iban = request.form["iban"]
        invoice_data.email = request.form["email"]
        invoice_data.mobile_nr = request.form["mobile_nr"]
        invoice_data.post_address = request.form["post_address"]
        if len(income.title) > 100:
            return render_template("error.html", message="Title is too long")
        if float(income.amount) > 1000:
            return render_template("error.html", message="Amount is too high")
        if float(income.price) > 200000:
            return render_template("error.html", message="Price is too high")
        if not check_iban(invoice_data.iban):
            return render_template("error.html", message="IBAN is invalid")
        if float(invoice_data.payment_term) > 300:
            return render_template("error.html",
                                   message="Payment term should be less than 300 days")
        if len(invoice_data.customer) > 100:
            return render_template("error.html", message="Customer name is too long")
        if len(invoice_data.email) > 320:
            return render_template("error.html", message="Email is too long")
        if len(invoice_data.mobile_nr) > 15:
            return render_template("error.html", message="Mobile number is too long")
        if len(invoice_data.post_address) > 100:
            return render_template("error.html", message="Post address is too long")
        invoice_data.record_id = records.add_record(income)
        records.add_invoice(invoice_data)
        return redirect("/records")

@app.route("/update_income/<int:record_id>", methods=["GET","POST"])
def update_income(record_id):
    if request.method == "GET":
        record_data = records.get_record_data(record_id)
        invoice_id = records.get_invoice_id(record_id)
        invoice_data_now = records.get_invoice_data(invoice_id)
        classes = records.get_record_classes(2)
        return render_template("update_income.html", classes = classes,
                               i = invoice_data_now, r = record_data)
    if request.method == "POST":
        validators.check_csrf(request.form["csrf_token"])
        income = records.Record()
        invoice_data = records.Invoice()
        income.record_id = record_id
        income.record_date = request.form["record_date"]
        income.record_class = request.form["record_class"]
        income.amount = request.form["amount"]
        income.price = request.form["price"]
        income.title = request.form["title"]
        invoice_data. record_id = record_id
        invoice_data.payment_term = request.form["payment_term"]
        invoice_data.customer = request.form["customer"]
        invoice_data.iban = request.form["iban"]
        invoice_data.email = request.form["email"]
        invoice_data.mobile_nr = request.form["mobile_nr"]
        invoice_data.post_address =request.form["post_address"]
        if len(income.title) > 100:
            return render_template("error.html", message="Title is too long")
        if float(income.amount) > 1000:
            return render_template("error.html", message="Amount is too high")
        if float(income.price) > 200000:
            return render_template("error.html", message="Price is too high")
        if not validators.check_iban(invoice_data.iban):
            return render_template("error.html", message="IBAN is invalid")
        if float(invoice_data.payment_term) > 300:
            return render_template("error.html",
                                   message="Payment term should be less than 300 days")
        if len(invoice_data.customer) > 100:
            return render_template("error.html", message="Customer name is too long")
        if len(invoice_data.email) > 320:
            return render_template("error.html", message="Email is too long")
        if len(invoice_data.mobile_nr) > 15:
            return render_template("error.html", message="Mobile number is too long")
        if len(invoice_data.post_address) > 100:
            return render_template("error.html", message="Post address is too long")
        records.update_record_data(income)
        records.update_invoice(invoice_data)
        return redirect("/records")

@app.route("/records")
def view_records():
    record_data = records.show_records()
    return render_template("records.html", value = record_data)

@app.route("/invoice/<int:invoice_id>")
def invoice(invoice_id):
    i_data = records.get_invoice_data(invoice_id)
    due_date = i_data.date + timedelta(days=i_data.payment_term)
    total_wo_vat = round(i_data.price * i_data.amount, 2)
    vat_price = round(0.01 * i_data.vat * total_wo_vat, 2)
    total = vat_price + total_wo_vat
    return render_template("invoice.html", i = i_data, due_date = due_date, vat_price = vat_price,
                           total = total, total_wo_vat = total_wo_vat)

@app.route("/remove_record/<int:record_id>", methods=["GET","POST"])
def remove_record(record_id):
    record_data = records.get_record_data(record_id)
    if request.method == "GET":
        total_wo_vat = round(record_data.price * record_data.amount, 2)
        vat_price = round(0.01 * record_data.vat * total_wo_vat, 2)
        total = round(total_wo_vat + vat_price, 2)
        return render_template("remove_record.html", r = record_data, total_wo_vat = total_wo_vat,
                               vat_price = vat_price, total = total)
    if request.method == "POST":
        validators.check_csrf(request.form["csrf_token"])
        records.remove_record_data(record_id, record_data.record_type)
        return redirect("/records")
