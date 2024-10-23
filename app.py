from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave secreta segura

@app.route('/')
def index():
    products = session.get('products', [])
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        products = session.get('products', [])
        
        # Generar un nuevo ID basado en la longitud de la lista de productos
        new_id = str(len(products) + 1)

        product_name = request.form['nombre']
        quantity = request.form['cantidad']
        price = request.form['precio']
        expiry_date = request.form['fecha_vencimiento']
        category = request.form['categoria']

        new_product = {
            'id': new_id,
            'nombre': product_name,
            'cantidad': quantity,
            'precio': price,
            'fecha_vencimiento': expiry_date,
            'categoria': category
        }
        products.append(new_product)
        session['products'] = products
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    products = session.get('products', [])
    product = next((p for p in products if p['id'] == product_id), None)

    if request.method == 'POST':
        product['nombre'] = request.form['nombre']
        product['cantidad'] = request.form['cantidad']
        product['precio'] = request.form['precio']
        product['fecha_vencimiento'] = request.form['fecha_vencimiento']
        product['categoria'] = request.form['categoria']
        session['products'] = products
        return redirect(url_for('index'))

    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<product_id>')
def delete_product(product_id):
    products = session.get('products', [])
    products = [p for p in products if p['id'] != product_id]
    session['products'] = products
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
