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

def print_info(info):
    if info.get_name() is None:
        click.echo(click.style('Symbol: {} not valid'.format(info.get_name()), fg='yellow'))
        return
    click.echo('{}'.format(get_current_date_and_time()))
    click.echo(info.get_name())
    change = '+' if info.get_change() >= 0 else '-'
    click.echo('{price} {price_change} ({percent_change})'.format(price=info.get_price(),
                                                                  price_change=info.get_change(),
                                                                  percent_change=info.get_percent_change()))

@click.group(invoke_without_command=True)
def main():
    while(True):
        sym = get_symbol_from_user()
        try:
            info = get_finance_info(sym)
        except urllib2.URLError as e:
            click.echo(click.style('URL Error: {}'.format(e), fg='red'))
            click.echo()
            continue
        print_info(info)
        click.echo()

if __name__ == '__main__':
    main()
