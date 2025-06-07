
from backend.bom import BOM
from backend.raw_materials import inventory_raw
from backend.semi_finished import semi_finished
finished_products = {}
finished_id = 1

def add_finished (name, category, price, quantity, sku):
  from backend.utils import add_sku
  global finished_id
  if name in finished_products:
    print(f"[!] Finished Product '{name}' already exists.")
    return
  if sku is None:
       sku = add_sku(name, category, inventory_raw,semi_finished)
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
  try:
    price = float(input(f"Enter a price for {prod_name}:")) * quantity
  except ValueError:
    print("[X] Invalid price input.")
    return
  category = "Finished Product"
  sku = None
  add_finished(prod_name, category, price, quantity, sku)

def view_finished_product():
  if not finished_products:
    print("[!] No Finished Product available.")
    return
  for product,details in finished_products.items():
    print(f"ID: {details['id']}, Name: {product}, Category: {details['category']}, "
      f"Price: ${details['price']: .2f}, Quantity: {details['quantity']}, SKU: {details['sku']}")

def edit_finished(finished_id, prod_name=None, category=None, price=None, quantity=None, sku=None):
  for old_name, details in list(finished_products.items()):
    if details['id'] == finished_id:
      new_name = prod_name.title() if prod_name else old_name
      if prod_name and prod_name != old_name:
        finished_products[new_name] = finished_products.pop(old_name)
        details = finished_products[new_name]
      if sku is not None:
        details['sku'] = sku
      if category is not None:
        details['category'] = category.title()
      if quantity is not None:
        details['quantity'] = round(float(quantity), 2)
      if price is not None:
        details['price'] = round(float(price), 2)
      print(f"[~] Finished Product {finished_id} Updated.")
      view_finished_product()
      return
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
