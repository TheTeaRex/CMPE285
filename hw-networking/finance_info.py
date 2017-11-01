import click
import datetime
import pytz
import urllib2
import yahoo_finance


def get_symbol_from_user():
    symbol = click.prompt('Please enter a symbol')
    return symbol

def get_finance_info(symbol):
    return yahoo_finance.Share(symbol)

def get_current_date_and_time():
    now = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
    return now.strftime('%a %b %d %H:%M:%S %Z %Y')

def print_info(info, sym):
    if info.get_name() is None:
        click.echo(click.style('Symbol: {} not valid'.format(info.get_name()), fg='yellow'))
        return
    click.echo('{}'.format(get_current_date_and_time()))
    click.echo('{} ({})'.format(info.get_name(), sym.upper()))
    change = '+' if info.get_change() >= 0 else '-'
    click.echo('{price} {price_change} ({percent_change})'.format(price=info.get_price(),
                                                                  price_change=info.get_change(),
                                                                  percent_change=info.get_percent_change()))

@click.group(invoke_without_command=True)
def main():
    again = True
    while(again):
        sym = get_symbol_from_user()
        try:
            info = get_finance_info(sym)
            print_info(info, sym)
        except urllib2.URLError as e:
            click.echo(click.style('There is a networking issue right now, please try again later.', fg='red'))
        click.echo()
        again = click.confirm('Would you like to try again?')
        click.echo()

if __name__ == '__main__':
    main()
