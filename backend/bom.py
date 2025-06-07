from backend.raw_materials import inventory_raw
from backend.utils import add_sku 
  
BOM = {}

def add_bom(prod_name, components):
  prod_name = prod_name.title()
  formatted_components = {}
  for comp_name, qty in components.items():
    formatted_name = comp_name.title()
    formatted_components[formatted_name] = round(float(qty), 2)
  BOM[prod_name] = formatted_components
  print(f"[+] BOM for '{prod_name}' Added/Updated Successfully")
  print(f"🔧 Components Required for '{prod_name}':")
  for comp_name, qty in formatted_components.items():
   print(f"   - {comp_name}: {qty}")

def view_bom(prod_name=None):
  if prod_name:
    prod_name = prod_name.title()
    if prod_name in BOM:
        print(f"\n📦 BOM for '{prod_name}':")
        for component, qty in BOM[prod_name].items():
            print(f"   - {component}: {qty}")
    else:
        print(f"[X] No BOM found for '{prod_name}'.")
  else:
    if not BOM:
      print("[!] No BOMs available.")
      return
    print("📋 All BOMs:")
    for product, components in BOM.items():
      print(f"\nBOM for '{product}':")
      for component, qty in components.items():
        print(f"  - {component}: {qty}")

def edit_bom(prod_name):
  prod_name = prod_name.title()
  if prod_name not in BOM:
    print(f"[X] BOM for '{prod_name}' NOT FOUND.")
    return

  print(f"🛠 Current BOM for '{prod_name}':")
  view_bom(prod_name)

  while True:
    action = input("\nDo you want to add, update or delete a component? (Type 'exit' to stop): ").strip().lower()
    if action == "exit":
      break
    elif action == "add":
      comp_name = input("Enter new component name: ").strip().title()
      if comp_name in BOM[prod_name]:
        print(f"[!] Component '{comp_name}' already exists. Use 'update' to change its quantity.")
      else:
        try:
          qty = float(input("Enter quantity: "))
          BOM[prod_name][comp_name] = round(qty, 2)
          print(f"[+] Added '{comp_name}' with quantity {qty}.")
        except ValueError:
          print("[X] Invalid quantity.")
    elif action == "update":
      comp_name = input("Enter component name to update: ").strip().title()
      if comp_name in BOM[prod_name]:
          try:
            qty = float(input("Enter new quantity: "))
            BOM[prod_name][comp_name] = round(qty, 2)
            print(f"[~] Updated '{comp_name}' to quantity {qty}.")
          except ValueError:
            print("[X] Invalid quantity.")
      else:
        print(f"[X] Component '{comp_name}' not found.")
    elif action == "delete":
      comp_name = input("Enter component name to delete: ").strip().title()
      if comp_name in BOM[prod_name]:
        BOM[prod_name].pop(comp_name)
        print(f"[-] Deleted component '{comp_name}'.")
      else:
        print(f"[X] Component '{comp_name}' not found.")
    else:
      print("[!] Invalid action. Choose 'add', 'update', 'delete', or 'exit'.")

  print(f"\n[✓] Final BOM for '{prod_name}':")
  view_bom(prod_name)

def check_bom_completeness(prod_name):
  prod_name = prod_name.title()
  if prod_name not in BOM:
    print(f"[X] BOM for '{prod_name}' not found.")
    return False

  complete = True
  print(f"\n🔍 Checking BOM completeness for: {prod_name}")
  print("--------------------------------------------------")

  for component, qty_needed in BOM[prod_name].items():
    component = component.title()
    if component not in inventory_raw:
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


