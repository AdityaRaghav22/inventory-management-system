from backend.raw_materials import inventory_raw

BOM = {}

def add_bom_component(prod_name, comp_name, qty):
  if not prod_name or not comp_name or qty is None:
    return False, "[X] Missing required fields"
  prod_name = prod_name.title()
  comp_name = comp_name.title()
  try:
    qty = round(float(qty), 2)
  except ValueError:
    return False, "[X] Invalid quantity"
  if prod_name not in BOM:
    BOM[prod_name] = {}
  BOM[prod_name][comp_name] = qty
  return True, f"[+] Component '{comp_name}' added/updated for '{prod_name}'"

def delete_bom_component(prod_name, comp_name):
  prod_name = prod_name.title()
  comp_name = comp_name.title()
  if prod_name in BOM and comp_name in BOM[prod_name]:
    BOM[prod_name].pop(comp_name)
    return True, f"[-] Component '{comp_name}' deleted from BOM of '{prod_name}'"
  return False, "[X] Component not found"

def update_bom_component(prod_name, comp_name, qty):
  prod_name = prod_name.title()
  comp_name = comp_name.title()
  try:
    qty = round(float(qty), 2)
  except ValueError:
    return False, "[X] Invalid quantity"
  if prod_name in BOM and comp_name in BOM[prod_name]:
    BOM[prod_name][comp_name] = qty
    return True, f"[~] Updated '{comp_name}' to {qty}"
  return False, "[X] Component not found in existing BOM"

def get_bom(prod_name):
  prod_name = prod_name.title()
  return dict(BOM.get(prod_name, {}))

def get_all_boms():
  return dict(BOM)

def check_bom_completeness(prod_name):
  prod_name = prod_name.title()
  if prod_name not in BOM:
      return False, f"[X] BOM for '{prod_name}' not found."
  completeness_report = []
  complete = True

  for component, qty_needed in BOM[prod_name].items():
    component = component.title()
    if component not in inventory_raw:
      completeness_report.append({
        "component": component,
        "status": "❌ Missing",
        "required": qty_needed,
        "available": 0
        })
      complete = False
    else:
      available = inventory_raw[component]["quantity"]
      status = "✅ Sufficient" if available >= qty_needed else "❌ Insufficient"
      completeness_report.append({
        "component": component,
        "status": status,
        "required": qty_needed,
        "available": available
      })
      if available < qty_needed:
        complete = False
  return complete, completeness_report

def delete_bom(prod_name):
  prod_name = prod_name.title()
  if prod_name in BOM:
    del BOM[prod_name]
    return True, f"[-] BOM for '{prod_name}' deleted."
  return False, "[X] BOM not found."
