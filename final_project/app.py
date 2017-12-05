from flask import Flask, render_template, request
import get_data
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    inputs = {}
    inputs['amount'] = float(request.form['invest_amt'])
    return render_template('result.html',
                            error='error message',
                            something='something')

if __name__=='__main__':
    app.run()
