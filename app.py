from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'hemanth'

# Mock data for products
products = [
    {'id': 1, 'name': '6pcs Brown cups', 'price': 99, 'image': '/static/images/btcups.jpg'},
    {'id': 2, 'name': 'White cups set', 'price': 129, 'image': '/static/images/wtset.jpg'},
    {'id': 3, 'name': 'Red snack set', 'price': 129, 'image': '/static/images/rsset.jpg'},
    {'id': 4, 'name': '2pcs soup cups', 'price': 99, 'image': '/static/images/bscups.jpg'},
    {'id': 5, 'name': 'Plastic boxes', 'price': 129, 'image': '/static/images/tboxes.jpg'},
    {'id': 6, 'name': '2pcs Brown cups', 'price': 99, 'image': '/static/images/btcup.jpg'},
    {'id': 7, 'name': '2pcs Green cups', 'price': 99, 'image': '/static/images/gtcups.jpg'},
    {'id': 8, 'name': '4pcs Glass bowls', 'price': 99, 'image': '/static/images/hcups.jpg'},
    {'id': 9, 'name': '2pcs Soup bowls', 'price': 99, 'image': '/static/images/sb.jpg'},
    {'id': 10, 'name': '3pcs White plates', 'price': 99, 'image': '/static/images/plates.jpg'},
    {'id': 11, 'name': '3pcs Plastic cups', 'price': 99, 'image': '/static/images/plasticcups.jpg'},
    {'id': 12, 'name': '4pcs Spoons', 'price': 99, 'image': '/static/images/spoons.jpg'},
    {'id': 13, 'name': '3pcs plates', 'price': 99, 'image': '/static/images/yplates.jpg'},
    {'id': 14, 'name': 'Brush stand', 'price': 99, 'image': '/static/images/plas.jpg'},
    {'id': 15, 'name': 'cups set', 'price': 99, 'image': '/static/images/homeset.jpg'},
    {'id': 16, 'name': 'Square plates','price': 99, 'image': '/static/images/splates.jpg'},
    {'id': 17, 'name': 'White cup', 'price': 99, 'image': '/static/images/wc.jpg'},
    {'id': 18, 'name': 'Red box', 'price': 99, 'image': '/static/images/redb.jpg'},
]

@app.route('/')
def home():
    if 'customer_name' not in session or 'customer_number' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['customer_name'] = request.form['customer_name']
        session['customer_number'] = request.form['customer_number']
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/address', methods=['GET', 'POST'])
def address():
    if request.method == 'POST':
        session['customer_address'] = request.form['customer_address']
        session['customer_pincode'] = request.form['customer_pincode']
        return redirect(url_for('order'))
    return render_template('address.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] -= 1
                if item['quantity'] <= 0:
                    cart.remove(item)
                break
        session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('try.html', cart=cart, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        if 'cart' not in session:
            session['cart'] = []
        cart_item = next((item for item in session['cart'] if item['id'] == product_id), None)
        if cart_item:
            cart_item['quantity'] += 1
        else:
            session['cart'].append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'quantity': 1})
        session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/order', methods=['POST', 'GET'])
def order():
    if 'cart' in session:
        order_history = session.get('order_history', [])
        order_history.append({
            'order_id': len(order_history) + 1,  # Mock order ID
            'names': session['cart'],
            'total': sum(item['price'] * item['quantity'] for item in session['cart']),
            'customer_name': session['customer_name'],
            'customer_number': session['customer_number'],
            'customer_address': session['customer_address'],
            'customer_pincode': session['customer_pincode'],
        })
        session['order_history'] = order_history
        session.pop('cart', None)  # Clear the cart
        session.modified = True

        # Debugging: print session contents
        print(f"Order History: {session.get('order_history')}")
        
    return render_template('order.html')



@app.route('/cart/history', methods=['GET'])
def order_history():
    orders = session.get('order_history', [])
    return render_template('history.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
