from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
  return render_template('dashboard.html', active_page='dashboard')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html', active_page= 'inventory')

@app.route('/orders')
def sales_orders():
    return render_template('orders.html', active_page= 'orders')

@app.route('/notifications')
def notifications():
    return render_template('notifiaction.html', active_page= 'notifications')

@app.route('/chat')
def chat():
    return render_template('chat.html', active_page= 'chat')

@app.route('/setting')
def settings():
    return render_template('settings.html', active_page= 'settings')

@app.route('/help')
def help():
    return render_template('help.html', active_page= 'help')

if __name__ == '__main__':
  app.run(host = "0.0.0.0", debug=True)