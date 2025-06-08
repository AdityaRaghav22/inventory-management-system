import random as r
from datetime import datetime
def get_valid_date():
  while True:
    date_str = input("Enter Date (DD-MM-YYYY): ")
    try:
      sales_order_date = datetime.strptime(date_str, "%d-%m-%Y").date()
      return str(sales_order_date)
    except ValueError:
      print("[X] Invalid date format. Please use DD-MM-YYYY.")
      
def get_all_skus(inventory_raw= None, semi_finished=None):
  skus = set()
  if inventory_raw is not None:
    for prod,details in inventory_raw.items():
      skus.add(details['sku'])
  if semi_finished is not None:
    for prod,details in semi_finished.items():
      skus.add(details['sku'])
  return skus
    
def add_sku(product_name, category, inventory_raw, semi_finished):
  prefix = category[:3].upper()
  base = product_name[:3].upper()
  existing_skus = get_all_skus(inventory_raw, semi_finished)
  for _ in range(100):
    sku = f"{prefix}-{base}{r.randint(100, 999)}"
    if sku not in existing_skus:
      return sku
  raise Exception("[X] Failed to generate unique SKU after 100 attempts.") 
  
def generate_order_id():
  from backend.sales_orders import sales_order  
  if not sales_order:
    return "ORD001"
  last_id = sorted(sales_order.keys())[-1]
  number = int(last_id.replace("ORD",""))
  new_number = number + 1
  return f"ORD{new_number:03d}"


