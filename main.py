from flask import Flask, render_template, request, session, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user,login_manager, LoginManager
from flask_login import login_required, current_user
from datetime import datetime

#My db connection 
local_server = True
app = Flask(__name__)
app.secret_key='12345678'



#for getting unique user accesss
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.init_app(app)

@login_manager.user_loader
def load_customer(customer_SSN):
    return Customer.query.get(int(customer_SSN))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/bank_database'
db = SQLAlchemy(app)

#here we will pass endpoints and run the fuction




class test(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100))

class Bank(db.Model):
    Branch = db.Column(db.String(50), primary_key=True)
    Address = db.Column(db.String(250))

class Account(UserMixin, db.Model):
    Account_id = db.Column(db.Integer, primary_key=True)
    Account_bal = db.Column(db.Float)
    Type = db.Column(db.String(10))
    Branch = db.Column(db.String(50), db.ForeignKey('bank.Branch'))
    Pin = db.Column(db.String(1000))

    def get_id(self):
            return self.Account_id

class Acc_cust(UserMixin, db.Model):
    Account_id = db.Column(db.Integer, db.ForeignKey('account.Account_id'), primary_key=True)
    SSN = db.Column(db.BigInteger,db.ForeignKey('customer.SSN'))

    def get_id(self):
            return self.Account_id

class Transaction(UserMixin, db.Model):
    Transaction_id = db.Column(db.BigInteger, primary_key=True)
    Payer_account = db.Column(db.Integer, db.ForeignKey('account.Account_id'))
    Receiver_account = db.Column(db.Integer, db.ForeignKey('account.Account_id'))
    Amount = db.Column(db.Float)
    Time = db.Column(db.DateTime)

    payer = db.relationship('Account', foreign_keys=[Payer_account])
    receiver = db.relationship('Account', foreign_keys=[Receiver_account])

    def get_id(self):
            return self.Transaction_id

class Customer(UserMixin, db.Model):
    SSN = db.Column(db.BigInteger,primary_key=True)
    Fname = db.Column(db.String(20))
    Lname = db.Column(db.String(20))
    Sex = db.Column(db.String(10))
    DOB = db.Column(db.Date)
    Address = db.Column(db.String(250))
    PhoneNo = db.Column(db.BigInteger)
    Password = db.Column(db.String(1000))

    def get_id(self):
            return self.SSN

with app.app_context():
    db.create_all()

#for home page
@app.route('/')
def index():
    return render_template('index.html')

#For Login page
@app.route('/login',methods=["POST","GET"])
def login_page():
    if request.method == "POST":
        SSN = request.form.get("SSN_num")
        Password = request.form.get("exampleInputPassword1")

        customer = Customer.query.filter_by(SSN=SSN).first()
        if customer and check_password_hash(customer.Password,Password):
            login_user(customer)
            return redirect(url_for('welcome_page'))
        else:

            return render_template('invalid_account.html')
    return render_template('login.html')

#For Signup page
@app.route('/signup',methods=["POST","GET"])
def signup_page():
    if request.method == "POST":
        SSN = request.form.get("SSN_num")
        Fname = request.form.get("input_first_name")
        Lname =request.form.get("input_last_name")
        Sex = request.form.get("inlineRadioOptions")
        DOB = request.form.get("Dateofbirth")
        Address = request.form.get("input_Address")
        PhoneNo = request.form.get("input_phone")
        Password = request.form.get("exampleInputPassword1")

        

        customer = Customer.query.filter_by(SSN=SSN).first()
        
        if customer:
            print("SSN already exists")
            return render_template('account_not_created.html')
        
        encpassword = generate_password_hash(Password)

        # new_customer = db.engine.execute(f"INSERT INTO  'customer' ('SSN','Fname','Lname','Sex','DOB','Address','PhoneNo','Password') VALUES ('{SSN}','{Fname}','{Lname}','{Sex}','{DOB}','{Address}','{PhoneNo}','{encpassword}')")

        new_customer = Customer(SSN=SSN, Fname=Fname, Lname=Lname, Sex=Sex, DOB=DOB, Address=Address, PhoneNo=PhoneNo, Password=encpassword)
        db.session.add(new_customer)
        db.session.commit()
        return render_template('account_created.html')

    return render_template('signup.html')

@app.route('/create_account', methods=["GET", "POST"])
@login_required
def create_account_page():
    branches = Bank.query.all()

    if request.method == "POST":
        Account_bal = 0
        Type = request.form.get("acc_type")
        Branch = request.form.get("Branch")
        Pin = request.form.get("acc_pin")
        SSN = current_user.SSN
        
        encpin = generate_password_hash(Pin)

        new_account = Account(Account_bal=Account_bal, Type=Type, Branch=Branch, Pin=encpin)
        db.session.add(new_account)
        db.session.commit()

        account_id = new_account.Account_id
        new_acc_cust = Acc_cust(Account_id=account_id, SSN=SSN)
        db.session.add(new_acc_cust)
        db.session.commit()
        return render_template('bank_account_created.html',name=current_user.Fname)
        
    return render_template('create_account.html', name=current_user.Fname, branches=branches)

@app.route('/withdraw_money', methods=["GET", "POST"])
@login_required
def withdraw_money_page():
    user_accounts = db.session.query(Account).join(Acc_cust).filter(Acc_cust.SSN == current_user.SSN).all()

    if request.method == "POST":
        Account_id = request.form.get("account")
        Amount = float(request.form.get("Amount"))
        Pin = request.form.get("acc_pin")

        account = Account.query.filter_by(Account_id=Account_id).first()

        if account and check_password_hash(account.Pin, Pin):
            if account.Account_bal < Amount:
                return render_template("withdraw_unsuccessful.html",name=current_user.Fname, bal=account.Account_bal)
            else:
                account.Account_bal -= Amount
                db.session.commit()
                return render_template('withdraw_successful.html',name=current_user.Fname, bal=account.Account_bal)
        else:
            return render_template('withdraw_failed.html',name=current_user.Fname)
    
    return render_template('withdraw_money.html', name=current_user.Fname, accounts=user_accounts)

@app.route('/deposit_money', methods=["GET", "POST"])
@login_required
def deposit_money_page():
    user_accounts = db.session.query(Account).join(Acc_cust).filter(Acc_cust.SSN == current_user.SSN).all()

    if request.method == "POST":
        Account_id = request.form.get("account")
        Amount = float(request.form.get("Amount"))
        Pin = request.form.get("acc_pin")

        account = Account.query.filter_by(Account_id=Account_id).first()

        if account and check_password_hash(account.Pin, Pin):
            account.Account_bal += Amount
            db.session.commit()
            return render_template('deposit_successful.html',name=current_user.Fname, bal=account.Account_bal)
        else:
            return render_template('deposit_failed.html',name=current_user.Fname)
    
    return render_template('deposit_money.html', name=current_user.Fname, accounts=user_accounts)

@app.route('/transfer_money', methods=["GET","POST"])
@login_required
def transfer_money_page():
    user_accounts = db.session.query(Account).join(Acc_cust).filter(Acc_cust.SSN == current_user.SSN).all()

    if request.method == "POST":
        Payer_account = request.form.get("payer_account")
        Receiver_account = request.form.get("rec_account")
        Amount = float(request.form.get("Amount"))
        Pin = request.form.get("acc_pin")
        payer_account = Account.query.filter_by(Account_id=Payer_account).first()
        receiver_account = Account.query.filter_by(Account_id=Receiver_account).first()

        if payer_account and check_password_hash(payer_account.Pin, Pin):
            if payer_account.Account_bal < Amount:
                return render_template("transfer_unsuccessful.html", name=current_user.Fname, bal=payer_account.Account_bal)
            elif not receiver_account:
                return render_template("transfer_not_valid.html", name=current_user.Fname)
            else:
                payer_account.Account_bal -= Amount
                receiver_account.Account_bal += Amount
                new_transaction = Transaction(Payer_account=Payer_account, Receiver_account=Receiver_account, Amount=Amount)
                db.session.add(new_transaction)
                db.session.commit()
                return render_template('transfer_successful.html', name=current_user.Fname, bal=payer_account.Account_bal)
        else:
            return render_template('transfer_failed.html', name=current_user.Fname)
    
    return render_template('transfer_money.html', name=current_user.Fname, accounts=user_accounts)

@app.route('/transaction_history')
@login_required
def transaction_history_page():
    # Fetch transactions where the current user is either the payer or the receiver
    transactions = db.session.query(Transaction).join(Account, Transaction.Payer_account == Account.Account_id)\
                     .filter((Account.Account_id == Acc_cust.Account_id) & (Acc_cust.SSN == current_user.SSN))\
                     .all()

    history = []

    for transaction in transactions:
        payer_name = db.session.query(Customer).join(Acc_cust, Customer.SSN == Acc_cust.SSN)\
                      .join(Account, Acc_cust.Account_id == Account.Account_id)\
                      .filter(Account.Account_id == transaction.Payer_account)\
                      .first().Fname

        receiver_name = db.session.query(Customer).join(Acc_cust, Customer.SSN == Acc_cust.SSN)\
                          .join(Account, Acc_cust.Account_id == Account.Account_id)\
                          .filter(Account.Account_id == transaction.Receiver_account)\
                          .first().Fname

        formatted_time = transaction.Time.strftime("%Y-%m-%d %H:%M:%S")

        history.append({
            'transaction_id': transaction.Transaction_id,
            'payer_name': payer_name,
            'receiver_name': receiver_name,
            'amount': transaction.Amount,
            'time': formatted_time
        })

    return render_template('transaction_history.html', name=current_user.Fname, history=history)

@app.route('/user_details')
@login_required
def user_details_page():
    customer_details = Customer.query.filter_by(SSN=current_user.SSN).first()
    accounts = db.session.query(Account).join(Acc_cust).filter(Acc_cust.SSN == current_user.SSN).all()
    return render_template('user_details.html', name=current_user.Fname, customer=customer_details, accounts=accounts)



@app.route('/account_list', methods=["GET", "POST"])
@login_required
def account_list_page():
    user_accounts = db.session.query(Account).join(Acc_cust).filter(Acc_cust.SSN == current_user.SSN).all()
    return render_template('account_list.html', name=current_user.Fname,accounts=user_accounts)


#For about us page
@app.route('/about')
def about_us_page():
    return render_template('about.html', name=current_user.Fname)

@app.route('/about_new')
def about_us_new_page():
    return render_template('about_new.html')

@app.route('/contact_us')
def contact_us_new_page():
    return render_template('contact_us.html')

#For contact us page 
@app.route('/contact')
def contact_us_page():
    return render_template('contact.html', name=current_user.Fname)

@app.route('/welcome')
def welcome_page():
    return render_template('welcome.html', name = current_user.Fname)

@app.route('/logout')
def logout_page():
    session.clear()
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/test')
def hello():
    try:
        test.query.all()
        return "My database is connected"
    except:
        return "My datebase is not connected"


app.run(debug=True)