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
                                   payment_term = favorites.payment_term, vat = favorites.vat, email = favorites.email, 
                                   mobile_nr = favorites.mobile_nr, post_address = favorites.post_address)
        return render_template("update_favorites.html")
    if request.method == "POST":
        user_id = request.form["user_id"]
        business_id = request.form["business_id"]
        iban = request.form["iban"]
        payment_term = request.form["payment_term"] if request.form["payment_term"] else None
        vat = request.form["vat"] if request.form["vat"] else None
        email = request.form["email"]
        mobile_nr = request.form["mobile_nr"]
        post_address =request.form["post_address"]
        users.update_favorites(user_id, business_id, iban, payment_term, vat, email, mobile_nr, post_address)
        return redirect("/")
    
@app.route("/add_cost", methods=["GET","POST"])
def add_cost():
    if request.method == "GET":
        return render_template("add_cost.html")
    if request.method == "POST":
        user_id = request.form["user_id"]
        record_date = request.form["record_date"]
        title = request.form["title"]
        record_class = request.form["record_class"]
        price = request.form["price"]
        records.add_cost(user_id, record_date, title, record_class, price)
        return redirect("/")