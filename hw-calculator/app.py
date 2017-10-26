from flask import Flask, render_template, request
import stock_profile_calculator
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    inputs = {}
    inputs['stock_symbol'] = str(request.form['symbol'])
    inputs['allotment'] = int(request.form['allotment'])
    inputs['final_price'] = float(request.form['final_price'])
    inputs['sell_comm'] = float(request.form['sell_comm'])
    inputs['initial_price'] = float(request.form['initial_price'])
    inputs['buy_comm'] = float(request.form['buy_comm'])
    inputs['tax'] = float(request.form['tax'])
    outputs = stock_profile_calculator.process_data(inputs)
    stock_profile_calculator.print_outputs(outputs)
    return render_template('process.html',
                            proceeds=outputs['proceeds'],
                            cost=outputs['cost'],
                            allotment=outputs['allotment'],
                            final_price=outputs['final_price'],
                            total_purchase_price=outputs['total_purchase_price'],
                            buy_comm=outputs['buy_comm'],
                            sell_comm=outputs['sell_comm'],
                            tax=outputs['tax'],
                            cap_gain=outputs['cap_gain'],
                            tax_on_cap_gain=outputs['tax_on_cap_gain'],
                            net_profit=outputs['net_profit'],
                            roi=outputs['roi'] * 100.00,
                            even=outputs['even'])

if __name__=='__main__':
    app.run()
