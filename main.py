import random as r
from datetime import datetime

inventory_raw = {}
raw_id_counter = 1
semi_finished = {}
semi_finish_id = 1
finished_products = {}
finished_id = 1
sales_order = {}
sales_order_status = {"Pending", "Processing", "Shipped","Delivered","Cancelled"}
def get_valid_date():
  while True:
    date_str = input("Enter Date (DD-MM-YYYY): ")
    try:
      sales_order_date = datetime.strptime(date_str, "%d-%m-%Y").date()
      return str(sales_order_date)
    except ValueError:
      print("[X] Invalid date format. Please use DD-MM-YYYY.")
def get_all_skus():
  skus = set()
  for item in inventory_raw.values():
    skus.add(item['sku'])
  for item in semi_finished.values():
    skus.add(item['sku'])
  return skus
def add_sku(product_name, category):
  prefix = category[:3].upper()
  base = product_name[:3].upper()
  existing_skus = get_all_skus()

  for _ in range(100):
      sku = f"{prefix}-{base}{r.randint(100, 999)}"
      if sku not in existing_skus:
          return sku
  raise Exception("[X] Failed to generate unique SKU after 100 attempts.") 
def view_raw():
    if not inventory_raw:
        print("[!] No Raw Material available.")
        return
    for name,details in inventory_raw.items():
        print(f"ID: {details['id']}, Name: {name}, Category: {details['category']}, "
              f"Price: ${details['price']: .2f}, Quantity: {details['quantity']}, SKU: {details['sku']}")
def add_raw (name, category, price, quantity, sku):
  global raw_id_counter
  inventory_raw[name] = {
      'id' : raw_id_counter,
      'category' : category,
      'price' : round(float(price), 2),
      'quantity' : round(float(quantity), 2),
      'sku' : add_sku(name, category)
  }
  raw_id_counter += 1
  print(f"[+]Raw Material Added: {name}")
def delete_raw_id(raw_id):
  for name, details in inventory_raw.items():
    if details['id'] == raw_id:
      inventory_raw.pop(name)
      print(f"[-] Raw Material '{name}' with ID {raw_id} Deleted Successfully.")
      return
  print(f"[X] Raw Material with ID {raw_id} NOT FOUND.")
def delete_raw_name(raw_name):
  if raw_name in inventory_raw:
    inventory_raw.pop(raw_name)
    print(f"[-] Raw Material with Name: {raw_name} \n    Deleted Successfully.")
  else :
    print(f"[X] Raw Material with ID {raw_name} NOT FOUND.")
def edit_raw(raw_id,name=None, category=None, price=None, quantity=None, sku=None):
  for raw_name, details in inventory_raw.items():
    if details['id']==raw_id:
      if name is not None and name != raw_name:
         inventory_raw[name]= inventory_raw.pop(raw_name)
         details = inventory_raw[name]
      if sku : details['sku']= sku
      if category: details['category']= category
      if quantity : details['quantity']= quantity
      if price : details['price']= price
      print(f"[~] Raw Material {raw_id} Updated.")
      view_raw()
      return
  print(f"[X] Raw Material With ID {raw_id} Not Found.")
def search_raw_name(raw_name=None,raw_SKU=None):
  if raw_name in inventory_raw:
    print(f"Raw Material with name: {raw_name} (FOUND)")
    return
  elif raw_SKU :
    for name, details in inventory_raw.items():
      if details['sku'] == raw_SKU:
        print(f"[✔] Raw Material with SKU: {raw_SKU} (FOUND)")
        return
  else:
    print("Raw Material with following details NOT FOUND")
def input_validation_raw():
  while True:
    name = input("Enter Raw Material Name: ").strip().title()
    if not name:
      print("[X] Name cannot be empty.")
      continue
    elif not name.isalpha():
      print("[X] Name must contain only letters.")
      continue
    print(f"[✓] Valid name: {name}")
    break
  while True:
    category = input("Enter Category for Raw Material: ").strip().title()
    if not category:
      print("[X] Category cannot be empty.")
      continue
    elif not category.isalpha():
      print("[X] Name must contain only letters.")
      continue
    print(f"[✓] Valid Category: {category}")
    break
  while True:
    try:
      quantity = int(input("Enter Quantity: "))
      if quantity <= 0:
        print("Quantity should be greater than 0.")
        continue
      print(f"[✓] Valid Quantity: {quantity}")
      break
    except ValueError:
      print("Quantity must be a valid number")
  while True:
    try:
      price = float(input("Enter Price(For One Quantity): "))
      if price <= 0:
        print("Price should be greater than 0.")
        continue
      print(f"[✓] Valid Price: {price}")
      print(f"Total Price for {quantity}: {price * quantity}")
      break
    except ValueError:
      print("Price must be a valid number")
  sku =add_sku(name,category)
  add_raw(name,category,price*quantity,quantity,sku )
  view_raw()
BOM = {}
def add_bom(prod_name, components):
    prod_name = prod_name.title()
    formatted_components = {}
    for comp_name, qty in components.items():
        formatted_name = comp_name.title()
        formatted_components[formatted_name] = qty
    BOM[prod_name] = formatted_components
    print(f"BOM for '{prod_name}' Added/Updated Successfully")
    print(f"Components Required for {prod_name}:")
    for comp_name, qty in formatted_components.items():
        print(f"   - {comp_name}: {qty}")
def view_bom(prod_name=None):
  if prod_name :
    if prod_name in BOM :
      print(f"\nBOM for{prod_name}")
      for component, qty in BOM[prod_name].items():
        print(f"   -{component}: {qty}")
    else:
      print(f"[X] No BOM found for '{prod_name}'.")
  else:
    if not BOM:
      print(f"No BOM found for {prod_name}")
      return
    print("All BOMs:")
    for product, components in BOM.items():
            print(f"\nBOM for '{product}':")
            for component, qty in components.items():
                print(f"  - {component}: {qty}")
def edit_bom(prod_name):
  if prod_name not in BOM:
    print(f"[X]{prod_name} NOT FOUND.")
    return
  print(f"Current BOM for {prod_name}.")
  view_bom(prod_name)
  while True:
    action = input("\nDo you want to add, update or delete a component? (Type 'exit' to stop): ").strip().lower()
    if action == "exit":
              break
    elif action == "add":
      comp_name = input("Enter new component name: ").strip()
      if comp_name in BOM[prod_name]:
        print(f"[!] Component '{comp_name}' already exists. Use 'update' to change its quantity.")
      else:
        qty = int(input("Enter quantity: "))
        BOM[prod_name][comp_name] = qty
        print(f"[+] Added '{comp_name}' with quantity {qty}.")
    elif action == "update":
      comp_name = input("Enter component name to update: ").strip()
      if comp_name in BOM[prod_name]:
        qty = int(input("Enter new quantity: "))
        BOM[prod_name][comp_name] = qty
        print(f"[~] Updated '{comp_name}' to quantity {qty}.")
      else:
        print(f"[X] Component '{comp_name}' not found.")
    elif action == "delete":
      comp_name = input("Enter component name to delete: ").strip()
      if comp_name in BOM[prod_name]:
        BOM[prod_name].pop(comp_name)
        print(f"[-] Deleted component '{comp_name}'.")
      else:
        print(f"[X] Component '{comp_name}' not found.")
  else:
    print("[!] Invalid action. Choose a/u/d or 'exit'.")
  print(f"\n[✓] Final BOM for '{prod_name}':")
  view_bom(prod_name)
def check_bom_completeness(prod_name):
    if prod_name not in BOM:
        print(f"[X] BOM for '{prod_name}' not found.")
        return False
    complete = True
    print(f"\n🔍 Checking BOM completeness for: {prod_name}")
    print("--------------------------------------------------")
    for component, qty_needed in BOM[prod_name.title()].items():
        if component.title() not in inventory_raw:
            print(f"[X] ❌ Component '{component}' is missing from inventory.")
            complete = False
        else:
            qty_available = inventory_raw[component]["quantity"]
            status = "✅ Sufficient" if qty_available >= qty_needed else "❌ Insufficient"
            print(f"🔧 {component}: Required = {qty_needed}, Available = {qty_available} → {status}")
            if qty_available < qty_needed:
                complete = False
    print("--------------------------------------------------")
    if complete:
        print(f"[✓] BOM for '{prod_name}' is complete and fulfillable.")
    else:
        print(f"[X] BOM for '{prod_name}' is incomplete or missing components.")
    return complete
def add_semi (name,category,price, quantity, sku):
  global semi_finish_id
  semi_finished[name] = {
    'id' : semi_finish_id,
    'category': category,
    'price' : round(float(price),2),
    'quantity' : round(float(quantity),2),
    'sku' : add_sku(name,category)
  }
  semi_finish_id += 1
  print(f"[✓] Semi-Finished Product '{name}' Added/Updated Successfully.")
def add_finished (name, category, price, quantity, sku):
  global finished_id
  finished_products[name] = {
      'id' : finished_id,
      'category' : category,
      'price' : round(float(price),2),
      'quantity' : round(float(quantity),2),
      'sku' : sku
  }
  finished_id += 1
  print(f"[+]Finished Product Added: {name}")
def produce_product(prod_name, quantity):
  prod_name = prod_name.title()
  if prod_name not in BOM:
      print(f"[X] BOM for '{prod_name}' not found.")
      return
  for component, qty_needed in BOM[prod_name].items():
      total_needed = qty_needed * quantity
      if component not in inventory_raw:
          print(f"[X] Component '{component}' missing from inventory.")
          return
      elif inventory_raw[component]["quantity"] < total_needed:
          print(f"[X] Not enough '{component}'. Needed: {total_needed}, Available: {inventory_raw[component]['quantity']}")
          return
  for component, qty_needed in BOM[prod_name].items():
      inventory_raw[component]["quantity"] -= qty_needed * quantity
      print(f"[~] Used {qty_needed * quantity} of '{component}'.")
  print(f"[✓] Produced {quantity} unit(s) of '{prod_name}'.")
  price = float(input(f"Enter a price for {prod_name}:"))*quantity
  category = "Finished Product"
  sku = add_sku(prod_name,category)
  add_finished(prod_name, category, price, quantity, sku)
def produce_semi_finished(prod_name, quantity_to_produce):
  prod_name = prod_name.title()
  if prod_name not in BOM:
      print(f"[X] BOM for '{prod_name}' does not exist.")
      return
  for component, qty_needed in BOM[prod_name].items():
      total_required = qty_needed * quantity_to_produce
      if component not in inventory_raw:
          print(f"[X] Component '{component}' is missing from inventory.")
          return
      if inventory_raw[component]['quantity'] < total_required:
          print(f"[X] Not enough '{component}'. Required: {total_required}, Available: {inventory_raw[component]['quantity']}")
          return
  for component, qty_needed in BOM[prod_name].items():
      total_required = qty_needed * quantity_to_produce
      inventory_raw[component]['quantity'] -= total_required
      print(f"[-] Used {total_required} of '{component}'.")
  price = float(input(f"Enter a price for {prod_name}:"))*quantity_to_produce
  category = "Semi-Finished"
  sku = add_sku(prod_name,category)
  add_raw(prod_name, category, price, quantity_to_produce, sku)
  add_semi(prod_name, category, price, quantity_to_produce, sku)
  print(f"[✓] Produced {quantity_to_produce} unit(s) of semi-finished product '{prod_name}'.")
def view_finished_product():
  if not finished_products:
    print("[!] No Raw Material available.")
    return
  for product,details in finished_products.items():
    print(f"ID: {details['id']}, Name: {product}, Category: {details['category']}, "
      f"Price: ${details['price']: .2f}, Quantity: {details['quantity']}, SKU: {details['sku']}")
def generate_order_id():
  if not sales_order:
    return "ORD001"
  last_id = sorted(sales_order.keys())[-1]
  number = int(last_id.replace("ORD",""))
  new_number = number + 1
  return f"ORD{new_number:03d}"
def add_sales_order(customer_name, items_dict, order_date=None, notes=""):
  order_id = generate_order_id()
  total_price = 0.0
  order_items = {}
  if order_date is None:
    order_date = str(datetime.now().strftime("%d-%m-%Y"))
  for product, qty in items_dict.items():
    if product not in finished_products:
      print(f"[X] Product '{product}' not found in finished inventory.")
      return
    if finished_products[product]['quantity'] < qty:
      available = finished_products[product]['quantity']
      print(f"[X] Not enough '{product}'. Requested: {qty}, Available: {available}")
      return
    unit_price = finished_products[product]['price']
    order_items[product] = {
      "quantity": qty,
      "unit_price": unit_price
    }
    total_price += qty * unit_price
  for product, qty in items_dict.items():
    finished_products[product]['quantity'] -= qty
    print(f"[-] Deducted {qty} of '{product}' from inventory.")
  sales_order[order_id] = {
    "customer_name": customer_name,
    "items": order_items,
    "order_date": order_date,
    "status": "Pending",
    "total_price": total_price,
    "notes": notes
  }

  print(f"[✓] Sales order {order_id} added successfully for '{customer_name}'. Total: ₹{total_price:.2f}")
def view_sales_orders():
  if not sales_order:
    print("No sales orders found.")
    return
  for order_id, order_data in sales_order.items():
    print(f"Order ID: {order_id}")
    print(f"Customer: {order_data['customer_name']}")
    print(f"Date: {order_data['order_date']}")
    print(f"Status: {order_data['status']}")
    print(f"Total Price: ₹{order_data['total_price']:.2f}")
    print("Items:")
    for product, details in order_data['items'].items():
        print(f"  - {product}: {details['quantity']} unit(s) at ₹{details['unit_price']} each")
    print("-" * 40)
def update_sales_order_status(order_id, new_status):
  if order_id not in sales_order:
    print(f"[X] Order ID '{order_id}' not found.")
    return  
  if new_status not in sales_order_status:
    print(f"[X] Invalid status '{new_status}'.")
    return
  sales_order[order_id]['status'] = new_status
  print(f"[✓] Order ID '{order_id}' status updated to '{new_status}'.")
add_raw("Wood", "Raw Material", 100, 500, "W001")
add_raw("Glue", "Raw Material", 50, 100, "G001")
view_raw()

add_bom("Chair", {"Wood": 10, "Glue": 2})
view_raw()
produce_semi_finished("Chair", 4)

add_bom("Table", {"Wood": 20, "Glue": 4})
produce_semi_finished("Table",1)
view_raw()

add_bom("Set" , {"Chair": 4, "Table": 1})
produce_product("Set", 1)

add_sales_order("John Doe", {"Set": 1}, order_date=None, notes="Delivery on 2023-10-15")
view_sales_orders()



