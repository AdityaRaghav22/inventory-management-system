from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/')
def dashboard():
  from backend.raw_materials import inventory_raw
  from backend.semi_finished import semi_finished
  from backend.finished import finished_products
  from backend.sales_orders import sales_order 
  raw_count = len(inventory_raw)
  semi_count = len(semi_finished)
  finished_count = len(finished_products)
  order_count = list(sales_order.items())[-5:]
  return render_template('dashboard.html',
                         raw_count=raw_count,
                         semi_count=semi_count,
                         finished_count=finished_count,
                         order_count=order_count,
                         active_page='home')

@app.route('/products', methods=['GET', 'POST'])
def inventory():
  from backend.raw_materials import inventory_raw, add_raw
  from backend.semi_finished import semi_finished, add_semi
  from backend.finished import finished_products, add_finished
  from backend.sales_orders import sales_order 
  
  if request.method == 'POST':
      item_type = request.form.get('type')
      name = request.form['name']
      category = request.form['category']
      price = request.form['price']
      quantity = request.form['quantity']
  
      if item_type == 'raw':
          add_raw(name, category, price, quantity, semi_finished)
      elif item_type == 'semi':
          add_semi(name, category, price, quantity)
      elif item_type == 'finished':
          add_finished(name, category, price, quantity)
  
      return redirect(url_for('inventory'))
  
  raw_count = len(inventory_raw)
  semi_count = len(semi_finished)
  finished_count = len(finished_products)
  order_count = list(sales_order.items())[-5:]

  raw_total = sum(details["quantity"]for name,details in inventory_raw.items())
  semi_total = sum(details["quantity"]for name,details in semi_finished.items())
  finished_total = sum(details["quantity"]for name,details in finished_products.items())
  
  return render_template('products.html',
                         inventory=inventory_raw,
                         semi_finished=semi_finished,
                         finished_products=finished_products,
                         raw_count=raw_count,
                         semi_count=semi_count,
                         finished_count=finished_count,
                         raw_total=raw_total,
                         semi_total=semi_total,
                         finished_total=finished_total,
                         order_count=order_count,
                         active_page='inventory')
  
  
@app.route('/bom')
def bom():
  from backend.raw_materials import inventory_raw
  from backend.semi_finished import semi_finished
  from backend.finished import finished_products
  from backend.sales_orders import sales_order 
  raw_count = len(inventory_raw)
  semi_count = len(semi_finished)
  finished_count = len(finished_products)
  order_count = list(sales_order.items())[-5:]
  return render_template('bom.html',
                         raw_count = raw_count,
                         semi_count = semi_count,
                         finished_count = finished_count,
                         order_count = order_count,
                         active_page='bom')

@app.route('/sales_order')
def sales_order():
  from backend.raw_materials import inventory_raw
  from backend.semi_finished import semi_finished
  from backend.finished import finished_products
  from backend.sales_orders import sales_order 
  raw_count = len(inventory_raw)
  semi_count = len(semi_finished)
  finished_count = len(finished_products)
  order_count = list(sales_order.items())[-5:]
  return render_template('sales_order.html',
                         raw_count = raw_count,
                         semi_count = semi_count,
                         finished_count = finished_count,
                         order_count = order_count,
                         active_page='sales_order')

@app.route('/notification')
def notification():
  from backend.raw_materials import inventory_raw
  from backend.semi_finished import semi_finished
  from backend.finished import finished_products
  from backend.sales_orders import sales_order 
  raw_count = len(inventory_raw)
  semi_count = len(semi_finished)
  finished_count = len(finished_products)
  order_count = list(sales_order.items())[-5:]
  return render_template('notification.html',
                         raw_count = raw_count,
                         semi_count = semi_count,
                         finished_count = finished_count,
                         order_count = order_count,
                         active_page='notification')

@app.route('/settings')
def settings():
  from backend.raw_materials import inventory_raw
  from backend.semi_finished import semi_finished
  from backend.finished import finished_products
  from backend.sales_orders import sales_order 
  raw_count = len(inventory_raw)
  semi_count = len(semi_finished)
  finished_count = len(finished_products)
  order_count = list(sales_order.items())[-5:]
  return render_template('settings.html',
                         raw_count = raw_count,
                         semi_count = semi_count,
                         finished_count = finished_count,
                         order_count = order_count,
                         active_page='settings')

if __name__ == '__main__':
  app.run(host = "0.0.0.0", debug=True)
   