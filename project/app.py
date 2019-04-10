
import os
from flask_mysqldb import MySQL,MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, IntegerField, FloatField, DateField, SelectField, SubmitField, DateTimeField
from wtforms.validators import Required, InputRequired, DataRequired, Optional, Length, Email, URL,NumberRange, EqualTo, Regexp
from flask_mail import Mail, Message

from werkzeug.utils import secure_filename
import datetime
from pathlib import Path

#basedir = os.path.adspath(os.path.dirname(__name__))

app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd() +'/static'+'/uploadsave'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cleaning_service'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config["SECRET_KEY"] = "hard to guess string"
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
bootstrap = Bootstrap(app)


app.config['MAIL_SERVER'] = "smtp.outlook.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True,
app.config['MAIL_USERNAME'] = 'ilovepython205@outlook.com'
app.config['MAIL_PASSWORD'] = 'python205'
app.config['MAIL_DEFAULT_SENDER'] = 'ilovepython205@outlook.com'
app.config['FLASKY_ADMIN']  = 'ilovepython205@outlook.com'
mail = Mail(app)

##############################################################
        # this is WTForm to create a form for different use
##############################################################
class loginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4,max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=10)])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")

class loginForm2(FlaskForm):
    username2 = StringField("Username", validators=[InputRequired(), Length(min=4,max=20)])
    password2 = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=10)])
    submit2 = SubmitField("Submit")

class registerForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4,max=20)])
    truename = StringField("Truename", validators=[InputRequired(), Length(min=4,max=20)])
    email = StringField("e-mail")
    birth = DateField("Birthday")
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=10)])
    idcard = StringField("ID card", validators=[InputRequired(), Length(min=4,max=20)])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")

class OrderForm(FlaskForm):
    servicetype = StringField("servicetype", validators=[InputRequired(), Length(min=4,max=20)])
    homeservicedetail = SelectField('Service Detail',
        choices=[('all', 'All service included')])
    officeservicedetail = SelectField('Service Detail',
        choices=[('normal', 'Normal'), ('deep', 'Deep')])
    locustservicedetail = SelectField('Service Detail',
        choices=[('ssolution', 'Spray Solution'), ('fsolution', 'Fogging/Fumigation Solution'), ('bsolution', 'Bait Solution')])
    waxservicedetail = SelectField('Service Detail',
        choices=[('tcleaning', 'Tile Care & Cleaning'), ('vwaxing', 'PythonVinyl Care & Waxing')])
    size = SelectField('Service size',
        choices=[('Small','Small'),('Medium','Medium'),('Large','Large')])
    date = SelectField('Service date',
        choices=[('7 days after','7 days after'), ('8 days after','8 days after'), ('9 days after','9 days after'), ('10 days after','10 days after'),
         ('11 days after','11 days after'), ('12 days after','12 days after'), ('13 days after','13 days after')])
    time = SelectField('Service time',
        choices=[('morning','morning'), ('afternoon','afternoon')])
    address = StringField("address", validators=[InputRequired(), Length(min=4,max=200)])
    ordertime = DateTimeField('ordertime', format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField("Submit")

##############################################################
        # this is a profile by using modal
##############################################################
def profile():
    try:
        session['userid']
        curr = mysql.connection.cursor()
        user = session['userid']
        curr.execute('SELECT * FROM user WHERE userID = %s'%user)
        userData = curr.fetchone()
        if Path(os.getcwd()+'/static/uploadsave/'+ str(session['username'])+ '.' +'png').exists():
            userData['photo'] =  'uploadsave/'+ str(session['username']) + '.' +'png'

        elif Path(os.getcwd()+'/static/uploadsave/'+ str(session['username'])+ '.' +'jpg').exists():
            userData['photo'] =  'uploadsave/'+ str(session['username'])+ '.' +'jpg'

        elif Path(os.getcwd()+'/static/uploadsave/'+ str(session['username'])+ '.' +'jpeg').exists():
            userData['photo'] =  'uploadsave/'+ str(session['username'])+ '.' +'jpeg'

        else:
            userData['photo'] = "images/icon 1.png"

        return userData
    except Exception:

        pass



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

##############################################
    #forget password then send email
##############################################
@app.route("/fgmail")
def fgmail():
   msg = Message('Hello', recipients = ['jason98792880@gmail.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"
    

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

    #######################################################
        # check if the post request has the file part
    #######################################################
        file = request.files['upload']
        if 'upload' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
        
        elif file.filename == '':
            flash('No selected file')

            return redirect(url_for('index'))
        elif file and allowed_file(file.filename):


            filename = str(session['username']) + '.' + secure_filename(file.filename).split('.')[-1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return render_template('index.html', data=profile())
    return redirect(url_for('upload_file'))

    #######################################################
        # this is home page
    #######################################################
@app.route("/")
def index():
    return render_template('index.html',data=profile())

    #######################################################
            # this is login page
    #######################################################
@app.route("/login" , methods=["GET", "POST"])
def login():
    form = loginForm()
    if request.method == 'POST':
        inputusername = request.form['username']
        inputpassword = request.form['password']
        
        curr = mysql.connection.cursor()
        curr.execute("SELECT * FROM user WHERE username=%s", (inputusername,))
        for e in curr.fetchall():
            username1 = (e['username'])

        currr = mysql.connection.cursor()
        currr.execute("SELECT * FROM user WHERE username=%s", (inputusername,))
        for e in currr.fetchall():
            userid1 = (e['userID'])

        try: 
            username1 == inputusername
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user WHERE username=%s", (inputusername,))
            for e in cur.fetchall():
                pw = e['password']
            if inputpassword == pw :
                session['username'] = inputusername
                session['userid'] = userid1

                flash("login success","success")
                return redirect(url_for('index'))
            else:
                flash("wrong password","error")
                return render_template('login.html', form=form)
        except UnboundLocalError: 
            flash("wrong username","error")
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

    #######################################################
        # this is register page
    #######################################################
@app.route("/register" , methods=["GET", "POST"])
def register():
    form = registerForm(request.form)
    if request.method == "POST":
        username = form.username.data
        truename = form.truename.data
        email = form.email.data
        birth = form.birth.data
        password = form.password.data
        idcard = form.idcard.data

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user ( username, truename, useremail, birthdate, password, IDcard)"
                        "VALUES (%s,%s,%s,%s,%s,%s)",
                        ( username, truename, email, birth, password, idcard))
            mysql.connection.commit()

            flash("success","success")
            return render_template('index.html')
        except Exception:
            flash("wrong input information, please check that is the Caps-Lock are actived","error")
            return render_template('register.html', form=form)

    return render_template('register.html' , form=form)

    #######################################################
        # this logout can back to the main page
    #######################################################
@app.route("/logout")
def logout():
    session.clear()
    return render_template('index.html')
    
    #######################################################
        # this is house cleaning page
    #######################################################
@app.route("/home")
def home():
    return render_template('home.html', data=profile())

    #######################################################
        # this is locust cleaning page
    #######################################################
@app.route("/locust")
def locust():
    return render_template('locust.html', data=profile())

    #######################################################
        # this is office cleaning page
    #######################################################
@app.route("/office")
def office():
    return render_template('office.html', data=profile())

    #######################################################
        # this is wax cleaning page
    #######################################################
@app.route("/wax")
def wax():
    return render_template('wax.html', data=profile())

    #######################################################
        # this is aboutus page
    #######################################################
@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html', data=profile())

    ######################################################################################################
        # this is order page after click order button in different dervice than go to the payment page
    ######################################################################################################
@app.route("/orderpage" ,methods=["GET", "POST"])
def orderpage():
    form = OrderForm(request.form)
    if 'orderid' in request.args:
        try:
            a = session['userid']
            order = request.args['orderid']
            session['servicetype'] = request.args['orderid']
            return render_template('orderpage.html' ,test=order ,form=form, data=profile())
        except KeyError:
            flash ('please login', 'danger')
            return redirect('login')
    if request.method == 'POST':
        creditno = request.form['textbox'] 

        ordertype = session['servicetype']
        address = request.form['address']
        size = request.form['size']
        date = request.form['date']
        time = form.time.data
        ordertime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pay = request.form['chk']
        pay2 = int(pay)

        if ordertype == 'home':
            if size == 'Small':
                price = '$200'
            elif size == 'Medium':
                price = '$500'
            else:
                price = '$1200'

        elif ordertype == 'office':
            if size == 'Small':
                price = '$1200'
            elif size == 'Medium':
                price = '$1900'
            else:
                price = '$2800'

        elif ordertype == 'locust':
            if size == 'Small':
                price = '$600'
            elif size == 'Medium':
                price = '$1000'
            else:
                price = '$2200'
        
        elif ordertype == 'wax':
            if size == 'Small':
                price = '$1800'
            elif size == 'Medium':
                price = '$1000'
            else:
                price = '$2600'

        if pay2 + 1 == 3 :
            creditno = 'N/A'
            pay3 = 'cash'
        else :
            pay3 = 'credit card'

        if ordertype == 'home':
            servicedetail = form.homeservicedetail.data
        elif ordertype == 'office':
            servicedetail = form.officeservicedetail.data
        elif ordertype == 'locust':
            servicedetail = form.locustservicedetail.data
        else:
            servicedetail = form.waxservicedetail.data



        return render_template('orderpayment.html',
        ordertype=ordertype, servicedetail=servicedetail, size=size, date=date, time=time, address=address, ordertime=ordertime,price=price, data=profile(),pay=pay3, creditno=creditno)

    return render_template('orderpage.html', data=profile())

    #######################################################
        # this is result page to show the result
    #######################################################
@app.route("/result" ,methods=["GET", "POST"])
def result():
    if request.method == 'POST':
        ordertype = request.form['ordertype']
        servicedetail = request.form['servicedetail']
        address = request.form['address']
        size = request.form['size']
        date = request.form['date']
        time = request.form['time']
        ordertime = request.form['ordertime']
        price = request.form['price']
        pay = request.form['pay']
        creditno = request.form['creditno']
        userid = session['userid']
        date2 = str(date)
        date3 = date2[:-11]

        date4 = int(date3)
        
        now = datetime.datetime.now()
        time_needed = datetime.timedelta(days=date4)
        arrdate = now + time_needed
        arrdate2 = arrdate.strftime("%y-%m-%d %H:%M:%S")


        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO orders ( userID, buydate, address, payment, creditcardtype, creditno, service, servicedetail, size, ordertime, section)"
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        ( userid, ordertime, address, pay,'N/A', creditno, ordertype, servicedetail, size, arrdate2, time))
            mysql.connection.commit()

            cur1 = mysql.connection.cursor()
            cur1.execute("INSERT INTO timetable2 ( date, section, userID, orderID)"
                        "VALUES (%s,%s,%s,%s)",
                        ( arrdate2, time, userid, 1))
            mysql.connection.commit()

            flash("success","success")
            return render_template('result.html', ordertype=ordertype, servicedetail=servicedetail, size=size, date=date, time=time, address=address, ordertime=ordertime, price=price, data=profile(),pay=pay, creditno=creditno)
        except Exception:
            flash("wrong input information, please check that is the Caps-Lock are actived","error")
            return render_template('orderpayment.html')

    return render_template('result.html', data=profile())

    #######################################################
        # this is admin page to login
    #######################################################
@app.route("/admin", methods=["GET", "POST"])
def admin():
    form = loginForm2()
    if request.method == 'POST':
        inputusername = request.form['username2']
        inputpassword = request.form['password2']
        
        curr = mysql.connection.cursor()
        curr.execute("SELECT * FROM admin WHERE adname=%s", (inputusername,))
        for e in curr.fetchall():
            username1 = (e['adname'])

        currr = mysql.connection.cursor()
        currr.execute("SELECT * FROM admin WHERE adname=%s", (inputusername,))
        for e in currr.fetchall():
            userid1 = (e['adminid'])
        try: 
            username1 == inputusername
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM admin WHERE adname=%s", (inputusername,))
            for e in cur.fetchall():
                pw = e['adpw']
            if inputpassword == pw :
                session['adusername'] = inputusername
                session['aduserid'] = userid1

                flash("login success","success")
                return render_template('adminpage.html')

            else:
                flash("wrong password","error")
                return render_template('admin.html', form=form)
        except UnboundLocalError: 
            flash("wrong username","error")
            return render_template('admin.html', form=form)

    return render_template('admin.html', form=form)


    ##########################################################################
        # this is all user table after click the alluser button in admin page
    ##########################################################################
@app.route("/adminalluser", methods=["GET", "POST"])
def adminalluser():
    try:
        session['aduserid']
        curad = mysql.connection.cursor()
        details = curad.execute("SELECT * FROM user ")
        result = curad.fetchall()
        return render_template('adminalluser.html', result=result, row=details)

    except KeyError:
        return render_template("index.html")

    ##############################################################################
        # this is all order table after click the allorder button in admin page
    ##############################################################################
@app.route("/adminallorder", methods=["GET", "POST"])
def adminallorder():
    try:
        session['aduserid']
        curad = mysql.connection.cursor()
        details = curad.execute("SELECT * FROM orders")
        result = curad.fetchall()
        return render_template('adminallorder.html', result=result, row=details)

    except KeyError:
        return render_template("index.html")
    

    ###############################################################
    # this is a admin page with three button to check the data
    ###############################################################
@app.route("/adminpage", methods=["GET", "POST"])
def adminpage():
    try:
        session['aduserid']
        return render_template('adminpage.html')

    except KeyError:
        return render_template("index.html")

        #######################################################
        # this delete order with a delete button
        #######################################################
@app.route("/delorder" , methods=['GET', 'POST'])
def delorder():
    if 'oid' in request.args:
        orderid = request.args['oid']
        curso = mysql.connection.cursor()
        curso.execute("DELETE FROM orders where orderID = %s ", (orderid,))
        mysql.connection.commit()
    return redirect('adminallorder')

    #######################################################
    # this delete user with a delete button
    #######################################################
@app.route("/deluser" , methods=['GET', 'POST'])
def deluser():
    if 'userid' in request.args:
        orderid = request.args['userid']
        curso = mysql.connection.cursor()
        curso.execute("DELETE FROM user where userID = %s ", (orderid,))
        mysql.connection.commit()
    return redirect('adminalluser')


if __name__ == "__main__":
    app.secret_key = "hard to guset"
    app.run(debug = True)

