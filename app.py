# app.py
from flask import Flask, render_template, redirect, url_for, flash, request, session
from models import db, User
from forms import RegistrationForm, LoginForm, EditUserForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registrasi berhasil!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = None  # Inisialisasi variabel user di sini
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Mencari pengguna berdasarkan email
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login Berhasil!', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Gagal! Pastikan email dan password benar.', category='error')
    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Login terlebih dahulu!', category='warning')
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('dashboard.html', users=users)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('User berhasil diupdate!', category='success')
        return redirect(url_for('dashboard'))
    return render_template('edit_user.html', form=form, user=user)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User sudah berhasil ditambahkan!', category='success')
        return redirect(url_for('dashboard'))
    return render_template('add_user.html', form=form)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User berhasil dihapus!', category='success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Anda berhasil keluar!', category='info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True) 