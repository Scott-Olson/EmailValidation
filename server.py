from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnections import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app=Flask(__name__)
app.secret_key = "ThisIsSecret!"


mysql = connectToMySQL('emailsdb')

print("all the users", mysql.query_db("SELECT * FROM users;"))
users = mysql.query_db("SELECT * FROM users;")

def emailcheck(email):
	for user in users:
		if user['email_address'] == email:
			return False
		else:
			return True
	return True


@app.route('/')
def landing():
	
	return render_template('index.html', users=users)

@app.route('/submit', methods=["POST"])
def formsubmit():
	if len(request.form['email']) < 1:
		flash("Email cannot be blank!")
		return redirect('/')

	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!")
		return redirect('/')

	elif emailcheck(request.form['email']) == False:
		flash("Invalid Email Address!")
		return redirect('/')
	else:
		print("-=-=-=-=-email valid, generating new entry-=-=-=-=-")
		query = "INSERT INTO users (email_address, created_at, edited_at) VALUES (%(email)s, NOW(), NOW());"
		data = {
				'email': request.form['email']
				}
		mysql.query_db(query, data)
		return redirect('/results')

@app.route('/results')
def results():
	users = mysql.query_db("SELECT email_address, created_at FROM users;")
	return render_template('results.html', users=users)

# @app.route('/delete', methods=['POST'])
# def deleteEmail():
# 	print("-=-=-=-=-email beign removed-=-=-=-=-")
# 	query = "DELETE FROM users WHERE user.id =(id)  VALUES (%(id)i);"
# 	data = {
# 			'email': request.form['email']
# 			}
# 	mysql.query_db(query, data)
# 	return redirect('/results')

if __name__ =='__main__':
	app.run(debug=True)




