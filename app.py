from flask import Flask, render_template, request, session, redirect, url_for
import constants as const


app = Flask(__name__)
app.secret_key = 'secretkey'

def qtd_users():
    cont = 0
    try:
      with open(const.USER_FILE_NAME, 'r') as file:
          for userdata in file:
            cont = cont + 1
      return cont
    except:
      return "Não existe nenhum usuario cadastrado"

def qtd_enquete():
    cont = 0
    try:
      with open(const.ENQUETE_FILE_NAME, 'r') as file:
          for enquetedata in file:
            cont = cont + 1
      return cont
    except:
      return "Não existe nenhuma enquete cadastrada"


@app.route('/')
def home():
    if not session.get('logged_in'):
       return render_template(const.LOGIN_FILE_NAME)
    else:
        return dashboard()

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
       return redirect(url_for('home'))
    else:        
       return render_template(const.DASHBOARD_FILE_NAME, user=session['username'], 
                              quantidade_user=qtd_users(), quantidade_enquete=qtd_enquete())

@app.route('/login', methods=['POST'])
def do_login():
    with open(USER_FILE_NAME) as file:
            for userdata in file:
                user = userdata.split(" ")
                if request.form['password'] == user[1] and request.form['username'] == user[0]:
                    session['logged_in'] = True
                    session['username'] = user[0]
                    return redirect(url_for('dashboard'))

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

    with open(USER_FILE_NAME, 'a') as file:
        file.write('{} {} \n'.format(user, password))

    return home()





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)