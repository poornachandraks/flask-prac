from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.model import Item, Users
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    #Purchase Item Logic
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item = Item.query.filter_by(name = purchased_item).first()
        if p_item:
            if current_user.can_purchase(p_item):
                p_item.buy(current_user)
                flash(f"Congratulations, you have bought {p_item.name} for {p_item.price}$", category="success")
            else:
                flash(f"Unfortunately, you cannot buy {p_item.name} for {p_item.price}$", category="danger")

    #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item = Item.query.filter_by(name = sold_item).first()
        if s_item:
            if current_user.can_sell(s_item):
                s_item.sell(current_user)
                flash(f"Congratulations, you have sold {s_item.name} for {s_item.price}$", category="success")
            else:
                flash(f"Unfortunately, you cannot sell {s_item.name} for {s_item.price}$", category="danger")
        

    if request.method == "GET":        
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner = current_user.id)
        return render_template("market.html", items=items, purchase_form = purchase_form, owned_items = owned_items, selling_form = selling_form)
    return redirect(url_for('market_page'))

@app.route("/register" , methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        created_user = Users(username = form.username.data, email_address = form.email_address.data, password = form.password1.data)
        db.session.add(created_user)
        db.session.commit()
        login_user(created_user)
        flash(f'Account Created Successfully! You are logged in as {created_user.username}', category='success')
        return redirect(url_for('market_page'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error in creating the user: {err_msg}', category = 'danger')
    
    return render_template("register.html", form = form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Invalid Username or Password', category='danger')
    return render_template("login.html", form = form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash('You have been successfully logged out', category='info')
    return redirect(url_for('home_page'))
