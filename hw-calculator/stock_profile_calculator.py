#!/usr/bin/python

import click


def get_user_input():
    inputs = {}
    inputs['stock_symbol'] = click.prompt('Please enter a stock symbol')
    inputs['allotment'] = click.prompt('Please enter the number of shares', type=int)
    inputs['final_price'] = click.prompt('Please enter the final share price ($)', type=float)
    inputs['sell_comm'] = click.prompt('Please enter the sell commission price ($)', type=float)
    inputs['initial_price'] = click.prompt('Please enter the initial share price ($)', type=float)
    inputs['buy_comm'] = click.prompt('Please enter the buy commission price ($)', type=float)
    inputs['tax'] = click.prompt('Please enter the capital gain tax rate (%)', type=float)
    print ''
    return inputs

def print_outputs(outputs):
    print '----------PROFIT REPORT----------'
    print 'Proceeds: ${:.2f}'.format(outputs['proceeds'])
    print 'Cost: ${:.2f}'.format(outputs['cost'])
    print 'Total Purchase Price: {} X ${} = ${}'.format(
        outputs['allotment'],
        outputs['final_price'],
        outputs['total_purchase_price']
    )
    print 'Buy Commission: ${:.2f}'.format(outputs['buy_comm'])
    print 'Sell Commission: ${:.2f}'.format(outputs['sell_comm'])
    print 'Tax on Captial Gain: {}% of ${:.2f} = ${:.2f}'.format(
        outputs['tax'],
        outputs['cap_gain'],
        outputs['tax_on_cap_gain']
    )
    print 'Net Profit: ${:.2f}'.format(outputs['net_profit'])
    print 'Return of Investment: {:.2f}%'.format(outputs['roi'] * 100)
    print 'Break even price per share: ${:.2f}'.format(outputs['even'])

def process_data(inputs):
    outputs = {}
    # merging the two dictionaries
    outputs.update(inputs)
    outputs['proceeds'] = inputs['allotment'] * inputs['final_price']
    outputs['total_purchase_price'] = inputs['allotment'] + inputs['initial_price']
    cost = inputs['allotment'] * inputs['initial_price'] + inputs['sell_comm'] + inputs['buy_comm']
    outputs['cap_gain'] = outputs['proceeds'] - cost
    outputs['tax_on_cap_gain'] = outputs['cap_gain'] * inputs['tax'] / 100.00
    outputs['cost'] = outputs['tax_on_cap_gain'] + cost
    outputs['net_profit'] = outputs['proceeds'] - outputs['cost']
    outputs['roi'] = (outputs['proceeds'] - outputs['cost']) / outputs['cost']
    outputs['even'] = cost / inputs['allotment']
    return outputs

@click.group(invoke_without_command=True)
def main():
    inputs = get_user_input()

    outputs = process_data(inputs)

    # print outputs
    print_outputs(outputs)

if __name__ == '__main__':
    main()
