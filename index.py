from flask import Flask,  render_template, flash, url_for, redirect,  request,json, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from forms import RegisForm, LoginForm, PasienForm, RawatForm
import string
import random


mysql = MySQL()
app = Flask(__name__)

app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SECRET_KEY']  = '60c14daa4a733bf2fd912d4d0043f5d6'
app.secret_key = 'why would I tell you my secret key?'
posts = [
    {'nama' : 'aria'},
    {'nama' : 'nurul'},
    {'nama' : 'nuria'},
]


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'dbrawat'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def checkSessions(data):
    if session.get('user') :
        return render_template(data)
    else :
        form = LoginForm()
        return render_template('login.html', posts= posts, form=form) 

def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''. join(random.choice(chars) for x in range(size))



@app.route("/")
def home():
  return checkSessions('home.html')



@app.route('/regis', methods=["GET", "POST"])
def regis():
    if session.get('user') :
        return redirect(url_for('home'))
    form = RegisForm()
    return render_template('regis.html', posts= posts, form=form)




@app.route('/registration', methods=["GET", "POST"])
def registration():
  
    form = RegisForm()
    if form.validate_on_submit():
        try:
            _name = request.form['username']
            _email = request.form['name']
            _password = request.form['password']

            # validate the received values
            if _name and _email and _password:
                
                # All Good, let's call MySQL
                _id = random_generator()
                conn = mysql.connect()
                cursor = conn.cursor()
                _hashed_password = generate_password_hash(_password)
                cursor.callproc('sp_createAdmin',(_email,_name,_hashed_password,_id))
                data = cursor.fetchall()

                if len(data) is 0:
                    conn.commit()
                    flash('Great Job', 'success')
                    return render_template('login.html', posts= posts, form=LoginForm())
                else:
                   
                    flash(f'{data[0]}', 'danger')
                    return render_template('regis.html', posts= posts, form=form)
        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()

        # flash(f'Account created for {form.username.data}!', 'success')
        # return redirect(url_for('home'))
    elif form.con_password.errors  :
         flash(f'{form.con_password.errors}', 'danger')
         return redirect(url_for('regis'))
   



@app.route('/login', methods=["GET", "POST"])
def login():
    if session.get('user') :
        return redirect(url_for('home'))
    form = LoginForm()
    return render_template('login.html', posts= posts, form=form) 


@app.route('/loginCheck', methods=["GET", "POST"])
def loginCheck():
    form = LoginForm()
    if form.validate_on_submit():
        try :
            con = mysql.connect()
            cursorLogin = con.cursor()
            _usernameLogin = request.form['name']
            _passwordPassword = request.form['password']
            cursorLogin.callproc('sp_validateLogin', (_usernameLogin,))
            data = cursorLogin.fetchall()
            
            if len(data) > 0 :
                # return json.dumps(str(data[0][3]))
                if check_password_hash(str(data[0][3]), _passwordPassword) :
                    session['user'] = data[0][2]
                    return redirect('/')
                else :
                    flash('Please Check Your Username Or Password', 'danger')
                    return redirect(url_for('login'))
            else :
                flash('Username Not Found', 'danger')
                return redirect(url_for('login'))
            return  json.dumps("ada")
        except Exception as e :
            return  json.dumps(str(e))
        finally :
            cursorLogin.close()
            con.close()

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/dataPasien')
def dataPasien():
    if session.get('user') :
        form = PasienForm()
        rawat = RawatForm()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_getAllData')
        datas = cursor.fetchall()

        datas_dict = []
        for data in datas :
            data_dict = {
                'kd_pasien' : data[0],
                'nama_pasien' : data[1],
                'jk' : data[2],
                'alamat' : data[3],
                'umur' : data[4],
                'tanggal' : data[5],
                'admin' : data[6]
            }
            datas_dict.append(data_dict)
        

        cursor.callproc('sp_getAllJoin')
        pasien = cursor.fetchall()

        pasien_dict = []
        for data in pasien :
            data_dict = {
                'kd_rawat' : data[6],
                'nama_pasien' : data[0],
                'nama_dokter' : data[1],
                'spesialis' : data[2],
                'nama_kamar' : data[3],
                'kelas' : data[4],
                'tanggal' : data[5]
            }
            pasien_dict.append(data_dict)
        # return json.dumps(pasien_dict)
        return render_template('pasien.html', pasien = datas_dict, form = form, rawat = rawat, join = pasien_dict)
    else :
        form = LoginForm()
        return render_template('login.html', posts= posts, form=form) 



@app.route('/tambahPasien', methods=['GET', 'POST'])
def tambahPasien():
    form = PasienForm()
    if form.validate_on_submit():
        try : 
            if session.get('user') : 
                _nama = request.form['nama']
                _umur = request.form['umur']
                _alamat = request.form['alamat']
                _jk = request.form['jk']
                if _nama != '' and _umur  != '' and _alamat != ''  and _jk != '': 
                    _kd   = 'P'+ _jk[0]  +  _umur   + random_generator(2)
                else :
                    flash('Data Kurang Lengkap', 'danger')
                    return redirect(url_for('dataPasien'))
                conn = mysql.connect()
                cursor = conn.cursor()  
                _user = session.get('user')
                cursor.callproc('sp_tambahPasien',(_kd, _nama, _jk, _alamat, _umur, _user ))
                data = cursor.fetchall()

                if len(data) is 0 :
                    conn.commit()
                    return redirect(url_for('dataPasien'))
                else :
                    flash('Terjadi Kesalahan', 'danger')
                    return redirect(url_for('dataPasien'))
            else : 
                flash('Terjadi Kesalahan', 'danger')
                return redirect(url_for('dataPasien'))
        except Exception as e :
            return json.dumps(str(e))
        finally :
            cursor.close()
            conn.close()
    else : 
        flash('Pastikan Seluruh Data Terisi', 'danger')
        return redirect(url_for('dataPasien'))

@app.route('/addDataPasien')
def addDataPasien():
    return render_template('addpasien.html')


@app.route('/editData', methods=['GET', 'POST'])
def editData():
    form = PasienForm()
    if session.get('user') :
        _id = request.form['id']
        _user = session.get('user')

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_ambilPasienID', (_id,))
        datas = cursor.fetchall()

        datas_dict = []
        for data in datas :
            data_dict = {
                'kd_pasien' : data[0],
                'nama_pasien' : data[1],
                'jk' : data[2],
                'alamat' : data[3],
                'umur' : data[4],
                'tanggal' : data[5],
                'admin' : data[6]
            }
            datas_dict.append(data_dict)
        
        return json.dumps(datas_dict)
    else :
        form = LoginForm()
        return render_template('login.html', posts= posts, form=form) 

@app.route('/editPasien', methods=['GET', 'POST'])
def editPasien():
    form = PasienForm()
    if form.validate_on_submit():
        try : 
            if session.get('user') : 
                _kd = request.form['editKD']
                _nama = request.form['nama']
                _umur = request.form['umur']
                _alamat = request.form['alamat']
                _jk = request.form['editJK']
                if _nama == '' and _umur  == '' and _alamat == ''  and _jk == '': 
                    flash('Data Kurang Lengkap', 'danger')
                    return redirect(url_for('dataPasien'))
                conn = mysql.connect()
                cursor = conn.cursor()  
                _user = session.get('user')
                cursor.callproc('sp_editPasien',(_nama,_kd, _jk,_alamat, _umur, _user))
                data = cursor.fetchall()
                if len(data) is 0 :
                    conn.commit()
                    flash('Anda Melakukan perubahan pada kode pasien ' + _kd, 'success')
                    return redirect(url_for('dataPasien'))
                else :
                    flash('Terjadi Kesalahan', 'danger')
                    return redirect(url_for('dataPasien'))
               
            else : 
                flash('Terjadi Kesalahan', 'danger')
                return redirect(url_for('dataPasien'))
        except Exception as e :
            return json.dumps(str(e))
        # finally :
        #     cursor.close()
        #     conn.close()
    else : 
        flash('Pastikan Seluruh Data Terisi', 'danger')
        return redirect(url_for('dataPasien'))


@app.route('/deletePasien', methods=['GET', 'POST'])
def deletePasien() :
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deletePasien',(_id,))
            result = cursor.fetchall()
 
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'An Error occured'})
        else : 
            flash('Terjadi Kesalahan', 'danger')
            return redirect(url_for('dataPasien'))
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/getDokter', methods=["GET", "POST"])
def getDoctor():
    try:
        # if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_getAllDoctor')
        datas = cursor.fetchall()
        datas_dict = []
        for data in datas :
            data_dict = {
                'kd' : data[0],
                'name' : data[1],
            }
            datas_dict.append(data_dict)
        return json.dumps(datas_dict)
        # else :
        #     return json.dumps({'status':'An Error occured'})
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/getKamar', methods=["GET", "POST"])
def getKamar():
    try:
        # if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_getAllKamar')
        datas = cursor.fetchall()
        datas_dict = []
        for data in datas :
            data_dict = {
                'kd' : data[0],
                'name' : data[1],
            }
            datas_dict.append(data_dict)
        return json.dumps(datas_dict)
        # else :
        #     return json.dumps({'status':'An Error occured'})
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/getPasien', methods=["GET", "POST"])
def getPasien():
    try:
        # if session.get('user'):
        _id = request.form['id']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_getPasien',(_id,) )
        datas = cursor.fetchall()
        datas_dict = []
        for data in datas :
            data_dict = {
                'kd' : data[0],
                'nama' : data[1],
                'jk' : data[2],
                'alamat' : data[3],
                'umur' : data[4],
            }
            datas_dict.append(data_dict)
        return json.dumps(datas_dict)
        # else :
        #     return json.dumps({'status':'An Error occured'})
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)
    