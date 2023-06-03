from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/loginAdmin')
def loginAdmin():
    return render_template('login_admin.html')

@app.route('/loginUser')
def loginUser():
    return render_template('login_user.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)