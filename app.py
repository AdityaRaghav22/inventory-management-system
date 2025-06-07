from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():
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

def inventory():
  from backend.raw_materials import inventory_raw
  from backend.semi_finished import semi_finished
  from backend.finished import finished_products
  return render_template('products.html', inventory_raw=inventory_raw, semi_finished=semi_finished, finished_products=finished_products, active_page='inventory')

if __name__ == '__main__':
  app.run(host = "0.0.0.0", debug=True)
   