from flask import Flask, render_template, request
import get_data
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    errors = []
    investments = ['e_invest', 'g_invest', 'i_invest', 'q_invest', 'v_invest']
    inputs = {}
    inputs['amount'] = float(request.form['invest_amt'])
    inputs['e_invest'] = request.form.get('e_invest')
    inputs['g_invest'] = request.form.get('g_invest')
    inputs['i_invest'] = request.form.get('i_invest')
    inputs['q_invest'] = request.form.get('q_invest')
    inputs['v_invest'] = request.form.get('v_invest')
    count = 0
    for item in investments:
        if inputs[item] is not None:
            count += 1
    if count == 0 or count > 2:
        errors.append('Please select 1 or 2 investments strategies')

    return render_template('result.html',
                            errors=errors,
                            something='something')


if __name__=='__main__':
    app.run()
