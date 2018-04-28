from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/index')
def isaas():
    return render_template('index.html')

@app.route('/New-Faces')
def isaas():
    return render_template('newFaces.html')

@app.route('/Detected-Faces')
def detectedFaces():
    return render_template('detectedFaces.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
