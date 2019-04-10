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

def qtd_tarefa():
    cont = 0
    try:
      with open(const.TAREFA_FILE_NAME, 'r') as file:
        for tarefadata in file:
          cont = cont + 1
      return cont
    except:
      return "Não existe nenhuma tarefa cadastrada"

# Titulo, Descriçao, Nome, Autor
@app.route('/tarefas') 
def tarefa():
	with open(const.TAREFAS_FILE_NAME, 'r') as file:
		print(file)
        
@app.route('/tarefas/nova-tarefa') 
def cadastro_tarefa():
  return render_template(const.NEW_TASK_FILE_NAME)

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
                              quantidade_user=qtd_users(), quantidade_tarefa=qtd_tarefa())

@app.route('/login', methods=['POST'])
def do_login():
  with open(const.USER_FILE_NAME) as file:
    for userdata in file:
      user = userdata.split(" ")
      if request.form['password'] == user[1] and request.form['username'] == user[0]:
        session['logged_in'] = True
        session['username'] = user[0]
        return redirect(url_for('dashboard'))

  return redirect(url_for('cadastro'))

@app.route('/logout')
def do_logout():
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

  with open(const.USER_FILE_NAME, 'a') as file:
    file.write('{} {} \n'.format(user, password))

    return home()

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=4000)