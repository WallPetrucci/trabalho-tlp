from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'secretkey'

@app.route('/')
def home():
    if not session.get('logged_in'):
       return render_template('login.html')
    else:
        return admin()

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
       return redirect(url_for('home'))
    else:        
       return render_template('admin.html', user=session['username'])

@app.route('/login', methods=['POST'])
def do_login():
    with open('users.txt') as file:
            for userdata in file:
                user = userdata.split(" ")
                if request.form['password'] == user[1] and request.form['username'] == user[0]:
                    session['logged_in'] = True
                    session['username'] = user[0]
                    return redirect(url_for('admin'))

    return redirect(url_for('cadastro'))

@app.route('/logout')
def do_logout():
    print(session.get('logged_in'))
    if session.get('logged_in'):       
       session.pop('logged_in', None)
       session.pop('username', None)
       session.clear()
       return redirect(url_for('home'))

    return home()

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    user = request.form['username'].strip()
    password = request.form['password'].strip()

    with open('users.txt', 'a') as file:
        file.write('{} {} \n'.format(user, password))

    return home()





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)