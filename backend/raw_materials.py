import random as r
from backend.utils import add_sku

inventory_raw = {}
raw_id_counter = 1

def view_raw():
  if not inventory_raw:
    print("[!] No Raw Material available.")
    return
  for name, details in inventory_raw.items():
    print(f"ID: {details['id']}, Name: {name}, Category: {details['category']}, "
          f"Price: ${details['price']: .2f}, Quantity: {details['quantity']}, SKU: {details['sku']}")

def add_raw(name, category, price, quantity, semi_finished):
  global raw_id_counter
  if name in inventory_raw:
    print(f"[!] Raw Material '{name}' already exists.")
    return
  sku = add_sku(name, category, inventory_raw, semi_finished)
  inventory_raw[name] = {
    'id': raw_id_counter,
    'category': category,
    'price': round(float(price), 2),
    'quantity': round(float(quantity), 2),
    'sku': sku
  }

  raw_id_counter += 1
  print(f"[+] Raw Material Added: {name}")

def delete_raw_id(raw_id):
  for name, details in list(inventory_raw.items()):
    if details['id'] == raw_id:
      inventory_raw.pop(name)
      print(f"[-] Raw Material '{name}' with ID {raw_id} Deleted Successfully.")
      return
  print(f"[X] Raw Material with ID {raw_id} NOT FOUND.")

def delete_raw_name(raw_name):
  if raw_name in inventory_raw:
    inventory_raw.pop(raw_name)
    print(f"[-] Raw Material with Name: {raw_name} Deleted Successfully.")
  else:
    print(f"[X] Raw Material with Name {raw_name} NOT FOUND.")

def edit_raw(raw_id, name=None, category=None, price=None, quantity=None, sku=None):
  for raw_name, details in list(inventory_raw.items()):
    if details['id'] == raw_id:
      if name is not None and name != raw_name:
          inventory_raw[name] = inventory_raw.pop(raw_name)
          details = inventory_raw[name]
      if sku is not None:
          details['sku'] = sku
      if category is not None:
          details['category'] = category
      if quantity is not None:
          details['quantity'] = round(float(quantity),2)
      if price is not None:
          details['price'] = round(float(price),2)

      print(f"[~] Raw Material {raw_id} Updated.")
      view_raw()
      return

    print(f"[X] Raw Material With ID {raw_id} Not Found.")

def search_raw(raw_name=None, raw_SKU=None):
  if raw_name is not None:
    if raw_name in inventory_raw:
        print(f"Raw Material with name: {raw_name} (FOUND)")
    else:
        print(f"Raw Material with name: {raw_name} NOT FOUND")
    return

  if raw_SKU is not None:
    for name, details in inventory_raw.items():
        if details['sku'] == raw_SKU:
            print(f"[✔] Raw Material with SKU: {raw_SKU} (FOUND)")
            return
    print(f"Raw Material with SKU: {raw_SKU} NOT FOUND")
    return

  print("Please provide either raw_name or raw_SKU to search.")

add_raw("Wood", "Wood", 100, 100, None)
add_raw("Iron", "Metal", 200, 200, None)
