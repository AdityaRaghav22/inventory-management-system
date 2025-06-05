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
def get_all_skus(inventory_raw, semi_finished):
  skus = set()
  for item in inventory_raw.values():
    skus.add(item['sku'])
  for item in semi_finished.values():
    skus.add(item['sku'])
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