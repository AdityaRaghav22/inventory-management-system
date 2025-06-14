
from backend.bom import BOM
from backend.raw_materials import inventory_raw
from backend.semi_finished import semi_finished
from backend.utils import add_sku
finished_products = {}
finished_id = 1

def add_finished (name, category, price, quantity):
  from backend.utils import add_sku
  name = name.title()
  category = category.title()
  if name in finished_products:
    finished_products[name]["quantity"] += round(float(quantity), 2)
    finished_products[name]["price"] += round(float(price), 2)
    print(f"[~] Updated existing Finished Product: {name}")
    return
  global finished_id
  sku =  add_sku(name, category, inventory_raw, semi_finished)
  if name in finished_products:
    print(f"[!] Finished Product '{name}' already exists.")
    return
  finished_products[name] = {
      'id' : finished_id,
      'category' : category,
      'price' : round(float(price),2),
      'quantity' : round(float(quantity),2),
      'sku' : sku
  }
  finished_id += 1
  print(f"[+]Finished Product Added: {name}")
  
def produce_product(prod_name, quantity, price_per_unit):
  prod_name = prod_name.title()
  quantity = round(float(quantity), 2)
  if prod_name not in BOM:
    print(f"[X] BOM for '{prod_name}' not found.")
    return False, f"BOM for '{prod_name}' not found."
  for component, qty_needed in BOM[prod_name].items():
    total_needed = qty_needed * quantity
    component = component.title()
    raw_qty = inventory_raw.get(component, {}).get("quantity", 0)
    semi_qty = semi_finished.get(component, {}).get("quantity", 0)
    total_available = raw_qty + semi_qty
    if total_available < total_needed:
      return False, f"[X] Not enough '{component}'. Needed: {total_needed}, Available: {total_available}"
  for component, qty_needed in BOM[prod_name].items():
    total_needed = qty_needed * quantity
    component = component.title()
    if component in inventory_raw and inventory_raw[component]["quantity"] >= total_needed:
      inventory_raw[component]["quantity"] -= total_needed
    elif component in semi_finished and semi_finished[component]["quantity"] >= total_needed:
      semi_finished[component]["quantity"] -= total_needed
    else:
      print(f"[X] Not enough '{component}'.")        
    print(f"[~] Used {total_needed} of '{component}'.")
  category = "Finished Product"
  total_price = float(price_per_unit) * quantity
  add_finished(prod_name, category, total_price, quantity)
  return True, f"[✓] Produced {quantity} unit(s) of '{prod_name}'."
  

def view_finished_product():
  if not finished_products:
    print("[!] No Finished Product available.")
    return
  for product,details in finished_products.items():
    print(f"ID: {details['id']}, Name: {product}, Category: {details['category']}, "
      f"Price: ${details['price']: .2f}, Quantity: {details['quantity']}, SKU: {details['sku']}")

def edit_finished(finished_id, prod_name=None, category=None, price=None, quantity=None, sku=None):
  found = False
  for finished_name, details in list(finished_products.items()):
    if details['id'] == finished_id:
      found = True
      if prod_name is not None and prod_name != finished_name:
        finished_products[prod_name] = finished_products.pop(finished_name)
        details = finished_products[prod_name]
      if category is not None:
        details['category'] = category
      if quantity is not None:
        try:
          details['quantity'] = round(float(quantity), 2)
        except (TypeError, ValueError):
          print(f"[X] Invalid quantity input: {quantity}")
      if price is not None:
        try:
          details['price'] = round(float(price), 2)
        except (TypeError, ValueError):
          print(f"[X] Invalid price input: {price}")
      print(f"[~] Finished Product {finished_id} Updated.")
      details['sku'] = add_sku(prod_name, category, inventory_raw, semi_finished)
      view_finished_product()
      return
  if not found:
    print(f"[X] Finished Product With ID {finished_id} Not Found.")
  
def delete_finished(finished_id):
  for name, details in list(finished_products.items()):
    if details['id'] == finished_id:
      del finished_products[name]
      print(f"[–] Finished Product '{name}' deleted.")
      return 
  print(f"[X] Finished Product with ID {finished_id} not found.")

def get_finished_by_sku(sku):
  for name, details in finished_products.items():
    if details['sku'] == sku:
      return name, details
  return None

