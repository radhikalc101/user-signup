from flask import Flask, request, redirect, render_template
import cgi
import re

app = Flask(__name__)

app.config['DEBUG'] = True  

@app.route("/signup", methods=['POST'])
def signup():
    user_name = request.form["username"]
    password = request.form["password"]
    varify_password = request.form["verifypassword"]
    email = request.form["email"]

    user_name = user_name.strip()
    password = password.strip()
    varify_password = varify_password.strip()
    
#The user leaves any of the following fields empty: username, password, verify password.

    usernameError = ''
    if user_name == '' or len(user_name) > 20 or  len(user_name) < 3:
        usernameError = "That's not a valid username"
        
#The user's username or password is not valid -- for example, 
# it contains a space character or it consists of less than 3 characters or more than 20 characters 
# (e.g., a username or password of "me" would be invalid).
    passwordError = ''
    if password == '' or len(password) > 20 or  len(password) < 3:
        passwordError = "That's not a valid password"
        

#The user's password and password-confirmation do not match.
    verifypasswordError = ''
    if varify_password == '' or password != varify_password:
        verifypasswordError= " Password does not match"
        
#The user provides an email, but it's not a valid email. Note: the email field may be left empty, 
# but if there is content in it, then it must be validated. 
# The criteria for a valid email address in this assignment are that it has a single @, a single ., 
# contains no spaces, and is between 3 and 20 characters long.
    emailError = ''
    atTheRateValidation = email.find('@') == -1 or (email.find('@') > -1 and email.count('@') > 1)
    DOtValidation = email.find('.') == -1 or (email.find('.') > -1 and email.count('.') > 1) 
    if len(email) > 20 or  len(email) < 3 or atTheRateValidation or DOtValidation:
    #if len(email) > 20 or  len(email) < 3 or ( not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))
        emailError= "That's not a valid email"
    if usernameError == '' and passwordError == '' and verifypasswordError == '' and emailError == '':
        return render_template('welcome_page.html', userName=user_name)
    else:
        return redirect("/?username="+user_name+"&email="+email+"&usernameError="+usernameError+"&passwordError="+passwordError+"&verifypasswordError="+verifypasswordError+"&emailError="+emailError)


@app.route("/")
def index():
    errors = {}
    errors['username'] = request.args.get("usernameError")
    errors['password'] = request.args.get("passwordError")
    errors['verifypassword'] = request.args.get("verifypasswordError")
    errors['email'] = request.args.get("emailError")
    if errors['username'] == None:
        errors['username'] = ""
    if errors['password'] == None:
        errors['password'] = ""
    if errors['verifypassword'] == None:
        errors['verifypassword'] = ""
    if errors['email'] == None:
        errors['email'] = ""
    

    username = request.args.get("username")
    if username == None:
        username = ""
    email = request.args.get("email")
    if email == None:
        email = ""
    return render_template('index.html', errors=errors, username=username,password=request.args.get("password"),verifypassword=request.args.get("verifypassword"),email=email)

app.run()