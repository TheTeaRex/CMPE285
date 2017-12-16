from flask import Flask, render_template, request
import get_data
from datetime import datetime
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/chart')
def chart():
    dt = datetime.now()
    version = dt.strftime("%s")
    return render_template('chart.html',
                           version = version)

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
    days = request.form['days']
    if days != '':
        days = int(days)
    else:
        days = 0
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
    total_now = 0
    purchase = {}
    total = {}
    profit = {}
    percent = {}
    look_back = [5, 10]

    if days != 0:
        look_back.append(days)

    days_look_back = ((days / 365) + 2) * 114 + days
    print days_look_back

    for stock in distribution:
        key = translation[stock]['name']

        i = 0
        while 1:
            try:
                # getting the stock price
                data[key] = get_data.parse_data(
                    get_data.get_range(
                        translation[stock]['ticker'],
                        start=get_data.get_x_days_back(days_look_back),
                        end=get_data.get_current_date()
                    )
                )
            except get_data.NoSuchTicker:
                # try only 4 times
                if i == 4:
                    raise
                else:
                    i += 1
                    continue
            if key in data:
                break

        # calculate the dollar distribution if bought at this momnet
        purchase_now[key] = {}
        purchase_now[key]['distribution'] = distribution[stock]
        purchase_now[key]['amt_dist'] = amount * distribution[stock] / 100
        purchase_now[key]['share'] = int(purchase_now[key]['amt_dist'] / data[key][-1]['close'])
        total_now += purchase_now[key]['share'] * data[key][-1]['close']


    for day in look_back:
        # calculate the dollar distribution if bought x business days ago
        total[day] = 0
        purchase[day] = {}

        for stock in distribution:
            key = translation[stock]['name']
            purchase[day][key] = {}
            purchase[day][key]['distribution'] = distribution[stock]
            purchase[day][key]['old_price'] = data[key][-day]['close']
            purchase[day][key]['amt_dist'] = amount * distribution[stock] / 100
            purchase[day][key]['share'] = int(purchase[day][key]['amt_dist'] / data[key][-day]['close'])
            purchase[day][key]['cur_price'] = data[key][-1]['close']
            purchase[day][key]['cur_value'] = data[key][-1]['close'] * purchase[day][key]['share']
            total[day] += purchase[day][key]['cur_value']

        profit[day] = total[day] - amount
        percent[day] = profit[day] / amount



    #plot weekly history graph
    x = []
    y = []
    history_purchase = {}
    history_total = {}
    history_day = [1,2,3,4,5]
    for day in history_day:
        # calculate the dollar distribution if bought x business days ago
        history_total[day] = 0
        history_purchase[day] = {}

        for stock in distribution:
            key = translation[stock]['name']
            history_purchase[day][key] = {}
            history_purchase[day][key]['distribution'] = distribution[stock]
            history_purchase[day][key]['old_price'] = data[key][-day]['close']
            history_purchase[day][key]['amt_dist'] = amount * distribution[stock] / 100
            history_purchase[day][key]['share'] = int(history_purchase[day][key]['amt_dist'] / data[key][-day]['close'])
            history_purchase[day][key]['cur_price'] = data[key][-1]['close']
            history_purchase[day][key]['cur_value'] = data[key][-1]['close'] * history_purchase[day][key]['share']
            history_total[day] += history_purchase[day][key]['cur_value']

        x.append(day)
        y.append(history_total[day])
    plt.figure()
    plt.plot(y)
    plt.xticks(range(len(x)), x)
    plt.xlabel('Look back days')
    plt.ylabel('Portfolio total value (USD)')
    plt.savefig('./static/MyFig.png')


    return render_template('result.html',
                            errors=[],
                            amount=amount,
                            data=data,
                            purchase_now=purchase_now,
                            total_now=total_now,
                            look_back=look_back,
                            purchase=purchase,
                            total=total,
                            profit=profit,
                            percent=percent)


if __name__=='__main__':
    app.run()
