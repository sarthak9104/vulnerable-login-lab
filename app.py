from flask import Flask, request, render_template_string, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Create DB
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("INSERT INTO users VALUES ('admin','password123')")
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        # ❌ VULNERABLE QUERY
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        result = c.execute(query).fetchone()
        
        if result:
            session['user'] = username
            message = "Login Successful!"
        else:
            message = "Invalid credentials"
        
        conn.close()
    
    return render_template_string('''
        <h2>Login Page</h2>
        <form method="POST">
            Username: <input name="username"><br><br>
            Password: <input name="password"><br><br>
            <button type="submit">Login</button>
        </form>
        <p>{{message}}</p>
    ''', message=message)
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome {session['user']}"
    return "Unauthorized"


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
