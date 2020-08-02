#!/usr/bin/python3

import cgi, cgitb
import re
cgitb.enable()

def addstock(db, name, amount):
    if amount == None:
        amount = 1
    if name not in db.keys():
        db[name] = amount
    else:
        db[name] += amount

def checkstock(db, name):
    if name:
        if name not in db.keys():
            db[name] = 0
        print('{0}: {1}'.format(name, db[name]))
    else:
        db = dict(sorted(db.items()))
        for k, v in db.items():
            if v != 0:
                print('{0}: {1}'.format(k, v))

def sell(db, name, sales, amount, price):
    if amount == None:
        amount = 1
    if name not in db.keys():
        print('ERROR')
    else:
        rest = db[name]
        rest -= amount
        if rest < 0:
            print('ERROR')
            return
        else:
            db[name] -= amount
        if price:
            sales += amount * price
    return sales

def checksales(sales):
    if isinstance(sales, int):
        print('sales: %d' % sales)
    else:
        print('sales: %.2f' % sales)

input_data = cgi.FieldStorage()
func_set = ['addstock', 'checkstock', 'sell', 'checksales', 'deleteall']

with open('/var/www/data/stock.txt', 'r') as f:
    inf = f.read()
    if inf:
        e = inf.split(',')
        e = [x for x in e if x != '']
        for i in range(len(e)):
            e[i] = e[i].split(':')
            e[i] = (e[i][0], int(e[i][1]))
        stock = dict(e)
    else:
        stock = {}

with open('/var/www/data/sales.txt', 'r') as f:
    s = f.read()
    if re.match(r'\d+\.\d*', s):
        sales = float(s)
    elif s:
        sales = int(s)
    else:
        sales = 0

print('Content-Type: text/html') # HTML is following
print('')                         # Leave a blank line

try:
    function = input_data.getvalue("function")
    name = input_data.getvalue("name")
    amount = input_data.getvalue("amount")
    price = input_data.getvalue("price")
    if price:
        if re.match(r'\d+\.\d*', price):
            price = float(price)
        else:
            price = int(price)
    if amount and (re.match(r'\d+\.\d*', amount) or float(amount) < 0) or (name and len(name) > 8) or (price and price <= 0) or function == None or function not in func_set:
        print('ERROR')
    else:
        if amount:
            amount = int(amount)
        if function == 'addstock':
            addstock(stock, name, amount)
        elif function == 'checkstock':
            checkstock(stock, name)
        elif function == 'sell':
            sales = sell(stock, name, sales, amount, price)
        elif function == 'checksales':
            checksales(sales)
        else:
            stock = None
            sales = 0
        if function != 'checkstock' and function != 'checksales':
            with open('/var/www/data/stock.txt', 'w') as f:
                if stock:
                    for k, v in stock.items():
                        f.write(k + ':' + str(v) + ',')
                else:
                    f.write('')
        if function == 'sell' or function == 'deleteall':
            with open('/var/www/data/sales.txt', 'w') as f:
                f.write(str(sales))
except:
    print('<output>Unexpected error occurred</output>')
    raise SystemExit(1)
#print('<output>{0} {1} {2}(s).</output>'.format(function, amount, name))
