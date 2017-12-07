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
    investments = {
        'e_invest': ['apple', 'adobe', 'nestle'],
        'g_invest': ['amazon', 'netflix', 'tesla'],
        'i_invest': ['microsoft', 'nvidia', 'walmart'],
        'q_invest': ['general_electric', 'home_depot', 'mcdonalds'],
        'v_invest': ['johnson', 'blizzard', 'disney']
    }
    translation = {
        'apple': {'name': 'Apple Inc.', 'ticker': 'aapl'},
        'adobe': {'name': 'Adobe Systems Incorporated', 'ticker': 'adbe'},
        'nestle': {'name': 'Nestle SA (ADR)', 'ticker': 'nsrgy'},
        'amazon': {'name': 'Amazon.com Inc.', 'ticker': 'amzn'},
        'netflix': {'name': 'Netflix Inc.', 'ticker': 'nflx'},
        'tesla': {'name': 'Tesla Inc.', 'ticker': 'tsla'},
        'microsoft': {'name': 'Microsoft Corporation', 'ticker': 'msft'},
        'nvidia': {'name': 'NVIDIA Corporation', 'ticker': 'nvda'},
        'walmart': {'name': 'Wal-Mart Stores Inc.', 'ticker': 'wmt'},
        'general_electric': {'name': 'General Electric Company', 'ticker': 'ge'},
        'home_depot': {'name': 'Home Depot Inc.', 'ticker': 'hd'},
        'mcdonalds': {'name': 'McDonald\'s Corporation', 'ticker': 'mcd'},
        'johnson': {'name': 'Johnson & Johnson', 'ticker': 'jnj'},
        'blizzard': {'name': 'Activision Blizzard Inc.', 'ticker': 'atvi'},
        'disney': {'name': 'Walt Disney Co.', 'ticker': 'dis'}
    }
    inputs = {}
    inputs['amount'] = float(request.form['invest_amt'])
    selected = {}
    count = 0
    for investment in investments:
        inputs[investment] = request.form.get(investment)
        if inputs[investment] is not None:
            selected[investment] = float(request.form.get(investment + '_percent'))
            count += 1

    if count == 0 or count > 2:
        return render_template('result.html', errors=['Please select 1 or 2 investment strategies'])

    count = 0
    for item in selected:
        count += selected[item]

    if count != 100:
        return render_template('result.html', errors=['Please make sure all selected investment strategies add up to 100%'])

    distribution = {}
    for item in selected:
        count = 0
        for stock in investments[item]:
            percent = float(request.form.get(stock))
            count += percent
            distribution[stock] = selected[item] * percent / 100

        if count != 100:
            return render_template('result.html', errors=['Please make sure all stocks in an investment strategy add up to 100%'])

    cur_prices = {}
    for stock in distribution:
        cur_prices[translation[stock]['name']] = get_data.parse_data(get_data.get_range(translation[stock]['ticker']))[-1]['close']
        cur_prices[translation[stock]['name']] = float('{:.2f}'.format(cur_prices[translation[stock]['name']]))

    return render_template('result.html',
                            errors=[],
                            cur_prices=cur_prices)


if __name__=='__main__':
    app.run()
