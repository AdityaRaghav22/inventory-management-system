from flask import Flask, render_template, request, redirect, url_for,flash

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
  from backend.raw_materials import inventory_raw, add_raw,edit_raw
  from backend.semi_finished import semi_finished, add_semi,edit_semi
  from backend.finished import finished_products, add_finished,edit_finished
  from backend.sales_orders import sales_order 
  if request.method == 'POST':
    action = request.form.get('action')
    item_type = request.form.get('type')
    
    
    name = request.form['name'].strip() 
    category = request.form['category'].strip() 
    price = request.form['price'] 
    quantity = request.form['quantity'] 

    if action == 'add':
        if item_type == 'raw':
            add_raw(name, category, price, quantity, semi_finished)
        elif item_type == 'semi':
            add_semi(name, category, price, quantity)
        elif item_type == 'finished':
            add_finished(name, category, price, quantity)

    elif action == 'edit':
      name = request.form['name'].strip() or None
      category = request.form['category'].strip() or None
      price = request.form['price'] or None
      quantity = request.form['quantity'] or None
      prod_id_raw = request.form.get('prod_id')
      if not prod_id_raw or not prod_id_raw.isdigit():
        return redirect(url_for('inventory'))
      item_id = int(prod_id_raw)
      if item_type == 'raw':
        edit_raw(item_id, name, category, price, quantity)

      elif item_type == 'semi':
        edit_semi(item_id, name, category, price, quantity)
      elif item_type == 'finished':
        edit_finished(item_id, name, category, price, quantity)

    elif action == 'delete':
      prod_id_raw = request.form.get('prod_id')
      if not prod_id_raw or not prod_id_raw.isdigit():
        return redirect(url_for('inventory'))
      item_id = int(prod_id_raw)
      if item_type == 'raw':
        from backend.raw_materials import delete_raw_id
        delete_raw_id(item_id)
      elif item_type == 'semi':
        from backend.semi_finished import delete_semi  
        delete_semi(item_id)
      elif item_type == 'finished':
        from backend.finished import delete_finished
        delete_finished(item_id)
      
      
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
   
@app.route('/bom', methods=['GET', 'POST'])
def bom():
  from backend.raw_materials import inventory_raw
  from backend.semi_finished import semi_finished
  from backend.finished import finished_products
  from backend.sales_orders import sales_order
  from backend.bom import (
    get_all_boms, get_bom,
    add_bom_component, update_bom_component, delete_bom_component,
    delete_bom, check_bom_completeness
)

  message = ""
  if request.method == "POST":
    action = request.form.get("action")
    prod_name = request.form.get("prod_name")
    component = request.form.get("component")
    quantity = request.form.get("quantity")

    if action == "add":
      success, msg = add_bom_component(prod_name, component, quantity)
    elif action == "update":
      success, msg = update_bom_component(prod_name, component, quantity)
    elif action == "delete":
      success, msg = delete_bom_component(prod_name, component)
    elif action == "delete_bom":
      success, msg = delete_bom(prod_name)
    elif action == "check":
      _, completeness = check_bom_completeness(prod_name)
      msg = "Check results below."
    else:
      success, msg = False, "[X] Unknown action"

    message = msg

  # Prepare data for frontend
  raw_count = len(inventory_raw)
  semi_count = len(semi_finished)
  finished_count = len(finished_products)
  order_count = list(sales_order.items())[-5:]
  all_products = list(get_all_boms().keys())
  all_inventory = list(inventory_raw.keys()) + list(semi_finished.keys())

  selected_prod = request.args.get("prod_name")
  selected_bom = get_bom(selected_prod) if selected_prod else {}

  return render_template("bom.html",
                          raw_count=raw_count,
                          semi_count=semi_count,
                          finished_count=finished_count,
                          order_count=order_count,
                          all_products=all_products,
                          all_inventory=all_inventory,
                          selected_prod=selected_prod,
                          selected_bom=selected_bom,
                          message=message,
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
   