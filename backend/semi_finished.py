from os import name
from backend.raw_materials import inventory_raw, add_raw
from backend.utils import add_sku
semi_finished = {}
semi_finish_id = 1

def add_semi (semi_name ,category,price, quantity):
  global semi_finish_id
  while True:
    if not semi_name:
      print("[X] Name cannot be empty.")
      continue
    elif not semi_name.isalpha():
      print("[X] Name must contain only letters.")
      continue
    print(f"[✓] Valid name: {semi_name}")
    break
  while True:
    if not category:
      print("[X] Category cannot be empty.")
      continue
    elif not category.isalpha():
      print("[X] Name must contain only letters.")
      continue
    print(f"[✓] Valid Category: {category}")
    break

  sku = add_sku(semi_name, category, inventory_raw, semi_finished)
  if name in semi_finished:
    print(f"[!] Semi-Finished Product '{name}' already exists.")
    return
  semi_finished[semi_name] = {
    'id' : semi_finish_id,
    'category': category,
    'price' : round(float(price),2),
    'quantity' : round(float(quantity),2),
    'sku' : sku
  }
  semi_finish_id += 1
  print(f"[✓] Semi-Finished Product '{name}' Added/Updated Successfully.")

def produce_semi_finished(prod_name, quantity_to_produce):
  from backend.bom import BOM
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
  try:
    unit_price = float(input(f"Enter a price for '{prod_name}': "))
  except ValueError:
    print("[X] Invalid price input.")
    return
  price = unit_price * quantity_to_produce
  category = "Semi-Finished"
  
  add_raw(prod_name, category, price, quantity_to_produce,semi_finished)
  add_semi(prod_name, category, price, quantity_to_produce)
  print(f"[✓] Produced {quantity_to_produce} unit(s) of semi-finished product '{prod_name}'.")

def view_semi(prod_name = None):
  if prod_name:
    prod_name = prod_name.title()
    if prod_name in semi_finished:
      print(f"\n Semi-Finished Product: {prod_name}")
      for key,value in semi_finished[prod_name].items():
        print(f"   - {key.capitalize()}: {value}")
    else:
      print(f"[X] No Semi-Finished Product found for '{prod_name}'.")
  else:
    if not semi_finished:
      print("[!] No Semi-Finished Product available.")
      return
    print("📋 All Semi-Finished Products:")
    for name, details in semi_finished.items():
      print(f"ID: {details['id']}, Name: {name}, Category: {details['category']}, "
            f"Price: ${details['price']:.2f}, Quantity: {details['quantity']}, SKU: {details['sku']}")

def delete_semi(semi_id):
    for prod_name, details in list(semi_finished.items()):
      if details['id'] == semi_id:
        del semi_finished[prod_name]
        print(f"[–] Semi Finished Product '{prod_name}' deleted.")
        return 
    print(f"[X] Semi Finished Product with ID {semi_id} not found.")
    
def edit_semi(semi_id, name=None, category=None, price=None, quantity=None, sku=None):
  found = False
  for semi_name, details in list(semi_finished.items()):
    if details['id'] == semi_id:
      found = True
      if name is not None and name != semi_name:
        semi_finished[name] = semi_finished.pop(semi_name)
        details = semi_finished[name]
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
      print(f"[~] Semi Finished Product {semi_id} Updated.")
      details['sku'] = add_sku(name, category, inventory_raw, semi_finished)
      view_semi()
      return
  if not found:
    print(f"[X] Semi Finished Product With ID {semi_id} Not Found.")
