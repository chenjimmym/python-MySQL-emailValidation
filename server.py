from flask import Flask, render_template, request, redirect, session
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'aSecret'
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'email_validation')
# an example of running a query
# print mysql.query_db("SELECT * FROM friendList")

@app.route('/')
def mainpage():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)
    # print emails
    query2 = "SELECT * FROM email_logs"
    email_logs = mysql.query_db(query2)
    if email_logs:
        index = len(email_logs) - 1
    else:
        index = 0
    return render_template('index.html', emails = emails, email_logs = email_logs, index = index)

@app.route('/check', methods=['POST'])
def check():
    session['msg'] = False
    forCheck = request.form['email']
    query = "SELECT * FROM emails WHERE email = :toCheck"
    toCheck = {'toCheck': forCheck}
    results = mysql.query_db(query, toCheck)
    query2 = "INSERT INTO `email_validation`.`email_logs` (`email_log`, `created_at`) VALUES (:toCheck, NOW());"
    mysql.query_db(query2, toCheck)
    if results:
        print results
        session['enteredEmail'] = results[0]['email']
        session['msg'] = True
    else:
        print "No Match"
    # print forCheck
    return redirect('/')

@app.route('/reset', methods=['POST'])
def deleteLogs():
    query = "DELETE FROM `email_validation`.`email_logs`"
    mysql.query_db(query)
    session['msg'] = False
    return redirect('/')

app.run(debug=True)