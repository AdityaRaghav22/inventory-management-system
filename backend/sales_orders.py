from datetime import datetime
from backend.finished import finished_products
from backend.utils import generate_order_id

sales_order = {}
sales_order_status = {"Pending", "Processing", "Shipped","Delivered","Cancelled"}

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