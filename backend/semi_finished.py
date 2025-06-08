from os import name
from backend.raw_materials import inventory_raw, add_raw
from backend.utils import add_sku
from backend.bom import BOM
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

def delete_semi(prod_name):
  prod_name = prod_name.title()
  if prod_name in semi_finished:
    del semi_finished[prod_name]
    print(f"[✓] Semi-Finished Product '{prod_name}' deleted.")
  else:
    print(f"[X] Semi-Finished Product '{prod_name}' not found.")
    
def edit_semi(semi_id,prod_name=None, category=None, price=None, quantity=None, sku=None):
  for old_name, details in list(semi_finished.items()):
    if details['id']==semi_id:
      new_name= prod_name.title() if prod_name is not None else old_name
      if prod_name is not None and prod_name!= old_name:
        semi_finished[new_name]= semi_finished.pop(old_name)
        details = semi_finished[new_name]
      if sku is not None: 
        details['sku']= sku
      if category is not None: 
        details['category']= category.title()
      if quantity is not None: 
        details['quantity'] = round(float(quantity), 2)
      if price is not None: 
        details['price'] = round(float(price), 2)
      print(f"[~] Semi Finished {semi_id} Updated.")
      view_semi(new_name if prod_name is not None else old_name)
      return
  print(f"[X] Semi Finished With ID {semi_id} Not Found.")

