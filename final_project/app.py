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
    amount = float(request.form['invest_amt'])
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
    # checking the stock distribution
    for item in selected:
        count = 0
        for stock in investments[item]:
            percent = float(request.form.get(stock))
            count += percent
            distribution[stock] = selected[item] * percent / 100

        if count != 100:
            return render_template('result.html', errors=['Please make sure all stocks in an investment strategy add up to 100%'])

    data = {}
    purchase_now = {}
    purchase_5 = {}
    purchase_10 = {}
    total_5 = 0
    total_10 = 0
    purchase_20 = {}
    total_20 = 0
    for stock in distribution:
        key = translation[stock]['name']
        # getting the stock price
        data[key] = get_data.parse_data(
            get_data.get_range(
                translation[stock]['ticker'],
                start=get_data.get_x_days_back(30),
                end=get_data.get_current_date()
            )
        )

        # calculate the dollar distribution if bought at this momnet
        purchase_now[key] = {}
        purchase_now[key]['distribution'] = distribution[stock]
        purchase_now[key]['amt_dist'] = amount * distribution[stock] / 100
        purchase_now[key]['share'] = int(purchase_now[key]['amt_dist'] / data[key][-1]['close'])

        # calculate the dollar distribution if bought 5 business days ago
        purchase_5[key] = {}
        purchase_5[key]['distribution'] = distribution[stock]
        purchase_5[key]['old_price'] = data[key][-5]['close']
        purchase_5[key]['amt_dist'] = amount * distribution[stock] / 100
        purchase_5[key]['share'] = int(purchase_5[key]['amt_dist'] / data[key][-5]['close'])
        purchase_5[key]['cur_price'] = data[key][-1]['close']
        purchase_5[key]['cur_value'] = data[key][-1]['close'] * purchase_5[key]['share']
        total_5 += purchase_5[key]['cur_value']

        # calculate the dollar distribution if bought 10 business days ago
        purchase_10[key] = {}
        purchase_10[key]['distribution'] = distribution[stock]
        purchase_10[key]['old_price'] = data[key][-10]['close']
        purchase_10[key]['amt_dist'] = amount * distribution[stock] / 100
        purchase_10[key]['share'] = int(purchase_10[key]['amt_dist'] / data[key][-10]['close'])
        purchase_10[key]['cur_price'] = data[key][-1]['close']
        purchase_10[key]['cur_value'] = data[key][-1]['close'] * purchase_10[key]['share']
        total_10 += purchase_10[key]['cur_value']

        # calculate the dollar distribution if bought 20 business days ago
        purchase_20[key] = {}
        purchase_20[key]['distribution'] = distribution[stock]
        purchase_20[key]['old_price'] = data[key][-20]['close']
        purchase_20[key]['amt_dist'] = amount * distribution[stock] / 200
        purchase_20[key]['share'] = int(purchase_20[key]['amt_dist'] / data[key][-20]['close'])
        purchase_20[key]['cur_price'] = data[key][-1]['close']
        purchase_20[key]['cur_value'] = data[key][-1]['close'] * purchase_20[key]['share']
        total_20 += purchase_20[key]['cur_value']

    profit_5 = total_5 - amount
    percent_5 = profit_5 / amount
    profit_10 = total_10 - amount
    percent_10 = profit_10 / amount
    profit_20 = total_20 - amount
    percent_20 = profit_20 / amount

    return render_template('result.html',
                            errors=[],
                            amount=amount,
                            data=data,
                            purchase_now=purchase_now,
                            purchase_5=purchase_5,
                            total_5=total_5,
                            profit_5=profit_5,
                            percent_5=percent_5,
                            purchase_10=purchase_10,
                            total_10=total_10,
                            profit_10=profit_10,
                            percent_10=percent_10,
                            purchase_20=purchase_20,
                            total_20=total_20,
                            profit_20=profit_20,
                            percent_20=percent_20)


if __name__=='__main__':
    app.run()
