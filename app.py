from flask import Flask, render_template, request, redirect, url_for,flash

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

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
  
    name = request.form.get("name", "").strip().title() 
    category = request.form.get("category", "").strip() 
    try:
      price = float(request.form.get("price", 0))
      quantity = float(request.form.get("quantity", 0))
    except ValueError:
      return "Price and quantity must be numbers.", 400
    if not name.isalpha() or not category.isalpha():
      return "Name and category must contain only letters.", 400

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
  selected_bom = {}
  selected_product = None
  completeness = None

  if request.method == "POST":
    action = request.form.get("action")
    prod_name = request.form.get("prod_name")
    prod_name = prod_name.title() if prod_name else ""
    
    comp_name = request.form.get("comp_name")
    quantity = request.form.get("qty")

    if action == "add":
      success, msg = add_bom_component(prod_name, comp_name, quantity)
    elif action == "update":
      success, msg = update_bom_component(prod_name, comp_name, quantity)
    elif action == "delete":
      success, msg = delete_bom_component(prod_name, comp_name)
    elif action == "delete_bom":
      success, msg = delete_bom(prod_name)
      selected_bom = {}
      selected_product = prod_name.title() if prod_name else ""
      msg = "[✔] BOM check complete"
    elif action == "check":
      _, completeness = check_bom_completeness(prod_name)
      selected_bom = completeness
      selected_product = prod_name.title() if prod_name else ""
      msg = "[✔] BOM check complete"
    else:
      success, msg = False, "[X] Unknown action"

    message = msg
    if action not in ["check", "delete_bom"]:
      selected_bom = get_bom(prod_name)
      selected_product = prod_name.title() if prod_name else ""
  boms = get_all_boms()

  raw_count = len(inventory_raw)
  semi_count = len(semi_finished)
  finished_count = len(finished_products)
  order_count = list(sales_order.items())[-5:]

  return render_template("bom.html",
      raw_count=raw_count,
      semi_count=semi_count,
      finished_count=finished_count,
      order_count=order_count,
      all_inventory=list(inventory_raw.keys()) + list(semi_finished.keys()),
      all_products=list(boms.keys()),
      selected_bom=selected_bom,
      selected_product=selected_product,
      completeness=completeness,
      boms=boms,
      message=message,
      active_page='bom'
  )
 
@app.route("/production", methods=["GET", "POST"])
def production():
  from backend.raw_materials import inventory_raw
  from backend.semi_finished import semi_finished
  from backend.finished import finished_products, produce_product
  from backend.bom import BOM, check_bom_completeness
  from backend.semi_finished import produce_semi_finished

  message = ""
  selected_product = None
  product_type = None
  bom_data = None
  max_producible = None

  if request.method == "POST":
    product_type = request.form.get("product_type", "").lower()
    selected_product = request.form.get("product_name", "").title()
    action = request.form.get("action")

    try:
      quantity = float(request.form.get("quantity", 0))
      price = float(request.form.get("price", 0))
    except ValueError:
      return "Quantity and price must be numbers.", 400

    if not selected_product or product_type not in ["finished", "semi"]:
        message = "[X] Please select a valid product and type."
    elif selected_product not in BOM:
        message = f"[X] BOM not found for {selected_product}."
    else:
      complete, completeness_report = check_bom_completeness(selected_product)

      if complete:
        bom_data = BOM[selected_product]

        # ✅ Calculate max producible quantity
        min_ratio = float('inf')
        for component, qty_needed in bom_data.items():
          available = 0
          if component in inventory_raw:
            available += inventory_raw[component]["quantity"]
          if component in semi_finished:
            available += semi_finished[component]["quantity"]
          if available == 0:
            min_ratio = 0
            break
          ratio = available / qty_needed
          min_ratio = min(min_ratio, ratio)
        max_producible = int(min_ratio)

        if action == "produce":
          if quantity > max_producible:
              message = f"[X] Cannot produce {quantity}. Only {max_producible} unit(s) can be produced."
          else:
            if product_type == "finished":
                produce_product(selected_product, quantity, price)
            elif product_type == "semi":
                produce_semi_finished(selected_product, quantity, price)
            flash(f"[✓] Produced {quantity} unit(s) of {selected_product}.", "success")
            return redirect("/production")
        elif action == "check":
          message = f"[✔] BOM check complete for {selected_product}."
      else:
        bom_data = {}
        message = f"[X] Incomplete BOM for {selected_product}. Please check inventory."

  # Load dropdown options
  all_products = list(BOM.keys())
  raw_count = len(inventory_raw)
  semi_count = len(semi_finished)
  finished_count = len(finished_products)
  order_count = []  # You can update this later if needed

  return render_template("production.html",
      raw_count=raw_count,
      inventory_raw=inventory_raw,
      semi_finished=semi_finished,
      finished_products=finished_products,
      semi_count=semi_count,
      finished_count=finished_count,
      order_count=order_count,
      all_products=all_products,
      selected_product=selected_product,
      product_type=product_type,
      bom_data=bom_data,
      max_producible=max_producible,
      message=message,
      active_page='production'
      
  )

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
   