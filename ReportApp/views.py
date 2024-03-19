"""
Routes and views for the flask application.
"""

from datetime import datetime

from flask import render_template, url_for, redirect, flash
from base64 import b64encode
# import 'request' to request data from html
from flask import request
from flask_security import login_user, current_user, logout_user



from ReportApp import app, db, login_manager
from ReportApp.tables import NetUsers, RoleType, Report


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
# signup page for staff
@app.route('/signupStaff', methods=['GET', 'POST'])
def signupStaff():
    msg = ""
    # after clicking submit button
    if request.method == 'POST':
        # store role types
        roles = ['Staff', 'Student']
        existing_roles = RoleType.query.all()
        existing_role_names = [role.name for role in existing_roles]
        for role_name in roles:
            if role_name not in existing_role_names:
                role = RoleType(name=role_name)
                db.session.add(role)
        db.session.commit()


        # check if user already exists
        user = NetUsers.query.filter_by(email=request.form['email']).first()
        msg = ""
        # if user already exists render the msg
        if user:
            msg = "User already exist"
            # render signupStaff.html if user exists
            return render_template('signupStaff.html', msg=msg)

        # if user doesn't exist

        # store the user to database
        user = NetUsers(Name=request.form['Name'], Surname=request.form['Surname'],email=request.form['email'], active=1, password=request.form['password'])
        # store the role
        role = RoleType.query.filter_by(id=1).first() # role number 1 = staff
        user.roles.append(role)

        # commit the changes to database
        db.session.add(user)
        db.session.commit()

        # login the user to the app
        # this user is current user
        login_user(user)
        # redirect to staff home page

        return render_template("StaffHome.html")

    # case other than submitting form, like loading the page itself
    else:
        return render_template("signupStaff.html", msg=msg)




# signup page for staff
@app.route('/signupClient', methods=['GET', 'POST'])
def signupClient():
    msg = ""
    # after clicking submit button
    if request.method == 'POST':
        # store role types
        roles = ['Staff', 'Student']
        existing_roles = RoleType.query.all()
        existing_role_names = [role.name for role in existing_roles]
        for role_name in roles:
            if role_name not in existing_role_names:
                role = RoleType(name=role_name)
                db.session.add(role)
        db.session.commit()


        # check if user already exists
        user = NetUsers.query.filter_by(email=request.form['email']).first()
        msg = ""
        # if user already exists render the msg
        if user:
            msg = "User already exist"
            # render signupStaff.html if user exists
            return render_template('signupClient.html', msg=msg)

        # if user doesn't exist

        # store the user to database
        user = NetUsers(Name=request.form['Name'], Surname=request.form['Surname'],email=request.form['email'], active=1, password=request.form['password'])
        # store the role
        role = RoleType.query.filter_by(id=2).first() # role number 2 = student
        user.roles.append(role)

        # commit the changes to database
        db.session.add(user)
        db.session.commit()

        # login the user to the app
        # this user is current user
        login_user(user)
        # redirect to staff home page

        return render_template("ClientHome.html")

    # case other than submitting form, like loading the page itself
    else:
        return render_template("signupClient.html", msg=msg)






@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ""
    if request.method == 'POST':
        # search user in database
        user = NetUsers.query.filter_by(email=request.form['email']).first()
        # if exist check password
        if user:
            if user.password == request.form['password']:
                # if password matches, login the user
                login_user(user)
                if 'Staff' in [role.name for role in current_user.roles]:
                    return render_template("StaffHome.html")
                elif 'Student' in [role.name for role in current_user.roles]:
                    return render_template("ClientHome.html")
                else:
                    # If the user's role is neither Staff nor Student
                    msg = "Invalid role"
                    return render_template("signin.html", msg=msg)
            # if password doesn't match
            else:
                msg = "Wrong password"

        # if user does not exist
        else:
            msg = "User doesn't exist"

    # If the request method is not POST or if any other condition fails, render the login template
    return render_template('signin.html', msg=msg)


@app.route('/logout')
def logout():
    logout_user()
    # Redirect to the home page or any other desired page after logout
    return redirect(url_for('home'))


@app.route('/ClientHome')
def ClientHome():
    """Renders the client home page."""
    return render_template("ClientHome.html", title="Client Home")

@app.route('/StaffHome')
def StaffHome():
    """Renders the staff home page."""
    return render_template("StaffHome.html", title="Staff Home")

@app.route('/reportfault', methods=['GET', 'POST'])
def reportfault():
    if request.method == 'POST':

        #Retrieving email from NetUsers table
        user = NetUsers.query.filter_by(email=current_user.email).first()

        # Requesting the file submitted by the user

        file = request.files['file']

         #Assigning Details submitted by the user to the tables fields
        upload = Report(status="Submitted",  email=user.email, Name=user.Name, Surname=user.Surname, filename=file.filename, data=file.read(), Location=request.form['location'], info=request.form['info'])
        db.session.add(upload)
        db.session.commit()
        return render_template("msg.html")
        # case other than submitting form, like loading the page itself
    else:
        return render_template('reportfault.html', title='Report App')

@app.route('/msg')
def msg():
    """Renders the message page."""
    return render_template(
        'msg.html',
        title='Message Page',
        year=datetime.now().year,
        message='Your message page.'
    )


# Admin display all Reports
@app.route('/allreport', methods=['GET'])
def allreport():
    # Fetch all records from the reports table
    all_records = Report.query.all()
    # Encode image data to base64
    for record in all_records:
        if record.filename.lower().endswith('.jpg') or record.filename.lower().endswith('.jpeg'):
            record.image_data = f"data:image/jpeg;base64,{b64encode(record.data).decode('utf-8')}"
        else:
            record.image_data = f"data:image/png;base64,{b64encode(record.data).decode('utf-8')}"

    return render_template('allreport.html', records=all_records)


# user update status
@app.route('/StatusUpdate/<int:user_id>', methods=['GET', 'POST'])
def StatusUpdate(user_id):
    user = Report.query.get_or_404(user_id)

    if request.method == 'POST':
        # Update the status field
        user.status = request.form['status']
        db.session.commit()

        # Redirect to the same page with updated data
        return redirect(url_for('StatusUpdate', user_id=user_id))

    return render_template('StatusUpdate.html', title='Report App', user=user)




# Admin display all Reports
@app.route('/Displayreport', methods=['GET'])
def Displayreport():
    # Fetch all records from the reports table
    all_records = Report.query.all()
    # Encode image data to base64
    for record in all_records:
        if record.filename.lower().endswith('.jpg') or record.filename.lower().endswith('.jpeg'):
            record.image_data = f"data:image/jpeg;base64,{b64encode(record.data).decode('utf-8')}"
        else:
            record.image_data = f"data:image/png;base64,{b64encode(record.data).decode('utf-8')}"

    return render_template('Displayreport.html', records=all_records)




