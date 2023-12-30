from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# app.logger.info('testing info log')
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///adopt-a-paw.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    happyCats = db.execute("SELECT COUNT(1) count FROM pets WHERE type = 'Cat' AND adopted = 1")[0]['count']
    happyDogs = db.execute("SELECT COUNT(1) count FROM pets WHERE type = 'Dog' AND adopted = 1")[0]['count']
    scheduledVisits = db.execute("SELECT COUNT(1) count FROM visits")[0]['count']
    return render_template("index.html", happyCats=happyCats, happyDogs=happyDogs, scheduledVisits=scheduledVisits)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = getFormValueByInputName('username')
        password = getFormValueByInputName('password')
        
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile/profile.html")


@app.route("/profile/account-settings", methods=["GET", "POST"])
@login_required
def accountSettings():
    """Show user his username and allow to change username or password"""

    # Gets username
    username = db.execute(
        "SELECT username FROM users WHERE id = ?;", session["user_id"]
    )[0]["userName"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        new_username = getFormValueByInputName("new-username")

        new_password = getFormValueByInputName("new-password")
        confirmation = getFormValueByInputName("confirmation")

        current_password = getFormValueByInputName("current-password")

        current_password_hash = db.execute(
            "SELECT hash FROM users WHERE id = ?;", session["user_id"]
        )[0]["hash"]

        # Ensure passwords are the same
        if not check_password_hash(current_password_hash, current_password):
            return apology("passwords are not the same", 403)

        elif new_username:
            # Ensure username is unique
            if len(
                db.execute(
                    "SELECT username FROM users WHERE username = ?;", new_username
                )
            ):
                return apology("username already in use", 403)

            # Update username
            db.execute(
                "UPDATE users SET username = ? WHERE id = ?;",
                new_username,
                session["user_id"],
            )

        if new_password:
            # Ensure password has atleast 8 characters
            if not len(new_password) >= 8:
                return apology("password need atleast 8 characters", 403)

            # Ensure passwords are the same
            elif not new_password == confirmation:
                return apology("passwords must be the same", 403)

            # Ensure new password is not the same as current password
            elif check_password_hash(current_password_hash, new_password):
                return apology("new password and current are the same", 403)

            # Update password
            db.execute(
                "UPDATE users SET hash = ? WHERE id = ?;",
                generate_password_hash(new_password),
                session["user_id"],
            )

        # Success message
        flash("Username changed!") if new_username else flash("Password changed!")

        return redirect("/profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("profile/account-settings.html", username=username)

@app.route("/profile/personal-settings", methods=["GET", "POST"])
@login_required
def personalSettings():
    # Gets data
    user = db.execute(
        "SELECT fullname, email, phone FROM users WHERE id = ?;", session["user_id"]
    )[0]
    
    if request.method == "POST":
        fullname = getFormValueByInputName("fullname")
        email = getFormValueByInputName("email")
        phone = getFormValueByInputName("phone")

        # Update password
        db.execute(
            "UPDATE users SET fullname = ?, email = ?, phone = ? WHERE id = ?;",
            fullname,
            email,
            phone,
            session["user_id"],
        )

        # Success message
        flash("Personal data updated!")

        return redirect("/profile")
    else:
        return render_template("profile/personal-settings.html", fullname=user['fullName'], email=user['email'], phone=user['phone'])

@app.route("/profile/visits", methods=["GET", "POST"])
@login_required
def visits():
    if request.method == "POST":
        id = getFormValueByInputName('id')
        petId = getFormValueByInputName('petId')
        db.execute("DELETE FROM visits WHERE id = ? AND petId = ? AND userId = ?", id, petId, session["user_id"])
        flash("Visit canceled successfully!")
        return redirect("/profile/visits")
    else:
        visits = db.execute("SELECT v.id, v.petId, v.date, p.name, p.type, p.size, p.age, p.gender FROM visits v INNER JOIN pets p ON v.petId = p.id INNER JOIN users u ON v.userId = u.id WHERE u.id = ?;", session["user_id"])
        return render_template("/profile/visits.html", visits=visits)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = getFormValueByInputName("username")
        password = getFormValueByInputName("password")
        confirmation = getFormValueByInputName("confirmation")
        fullname = getFormValueByInputName("fullname")
        email = getFormValueByInputName("email")
        phone = getFormValueByInputName("phone")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)
        
        if not fullname:
            return apology("must provide full name", 400)
        
        if not email:
            return apology("must provide email", 400)

        if not phone:
            return apology("must provide phone", 400)

        # Ensure username is unique
        elif len(
            db.execute("SELECT userName FROM users WHERE username = ?;", username)
        ):
            return apology("username already in use", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password has atleast 8 characters
        elif not len(password) >= 8:
            return apology("password need atleast 8 characters", 400)

        # Ensure password and confirmation are the same
        elif not password == confirmation:
            return apology("passwords must be the same", 400)

        # Insert the new user into users and store a hash of the user’s password
        db.execute(
            "INSERT INTO users (username, hash, fullname, email, phone) VALUES (?, ?, ?, ?, ?);",
            username,
            generate_password_hash(password),
            fullname,
            email,
            phone
        )

        # Success message
        flash("Registered!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/adopt", methods=["GET", "POST"])
@login_required
def adopt():
    if request.method == "POST":
        petId = getFormValueByInputName("petId")
        date = getFormValueByInputName("date")
        hour = getFormValueByInputName("hour")
        
        if not petId or not date or not hour:
            return apology("must provide all values in the form", 400)
        
        scheduledDatetime = datetime.strptime("%s %s" % (date, hour), '%Y-%m-%d %H:%M')
        
        errorMessage = ''
        if scheduledDatetime.date() < datetime.now().date():
            errorMessage = "date must be greater than the current date"
            
        if scheduledDatetime.hour < 9 or scheduledDatetime.hour > 18:
            errorMessage = "hour must be greater than 9 and less than 18"
        
        if scheduledDatetime.minute != 0:
            errorMessage = "minutes must be equal to 0"
        
        haveVisitsScheduled = db.execute("SELECT COUNT(1) count FROM visits WHERE petId = ? AND date = ?;", petId, scheduledDatetime)[0]['count']
       
        if haveVisitsScheduled > 0:
            errorMessage = "this pet already has a visit scheduled for the selected time"
        
        if errorMessage:
            pets = getAvailablePets()
            return render_template("adopt.html", pets=pets, petId=petId, date=date, hour=hour, errorMessage=errorMessage)        
        else:
            db.execute("INSERT INTO visits (userId, petId, date) VALUES (?, ?, ?);", session["user_id"], petId, scheduledDatetime)
            flash("Visit scheduled successfully!")
            return redirect('/profile/visits')
    else:
        pets = getAvailablePets()
        return render_template("adopt.html", pets=pets)

@app.route("/pet/<int:id>")
@login_required
def petDetail(id):
    pet = db.execute("SELECT name, type, age, size, gender, about FROM pets WHERE id = ?", id)[0]
    
    if not pet:
        return apology("pet not found", 400)
    
    return {
        "id": id,
        "name": pet['name'],
        "type": pet['type'],
        "age": pet['age'],
        "size": pet['size'],
        "gender": pet['gender'],
        "about": pet['about'],
    }

@app.route("/about-us")
def aboutUs():
    return render_template("about-us.html")

@app.route("/contact-us", methods=["GET", "POST"])
def contactUs():
    if request.method == "POST":
        name = getFormValueByInputName("name")
        email = getFormValueByInputName("email")
        phone = getFormValueByInputName("phone")
        topic = getFormValueByInputName("topic")
        message = getFormValueByInputName("message")
                
        if not name or not email or not phone or not topic or not message:
            return apology("must provide all values in the form", 400)
        
        if topic not in ("how-to-help", "adoption", "other"): 
            return apology("invalid topic", 400)
        
        db.execute(
            "INSERT INTO contacts (fullname, email, phone, topic, message) VALUES (?, ?, ?, ?, ?);",
            name,
            email,
            phone,
            topic,
            message
        )

        flash("Email successfully sent!")

        return render_template("contact-us.html", submissionSuccessful=True)
    else:
        return render_template("contact-us.html")

def getFormValueByInputName(key):
    return request.form.get(key)

def getAvailablePets():
    return db.execute("SELECT * FROM pets WHERE adopted = 0 ORDER BY type, name;")