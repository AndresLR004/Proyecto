#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime 
# import flask_sqlalchemy import SQLAlchemy

import sqlite3

connection = sqlite3.connect('database/ProyectoA.db')
cursor = connection.cursor()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p"

@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def helloW(name=None):
    return render_template('hello.html', name=name)

@app.route('/')
def index():
    conn = sqlite3.connect(connection)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/products/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']

        conn = sqlite3.connect(connection)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio) VALUES ($n, $n)", (nombre, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/product/read/<int:id>')
def read_product(id):
    conn = sqlite3.connect(connection)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conn.close()

    if producto is None:
        return "Producto no encontrado", 404
    return render_template('products/read.html', producto=producto)

@app.route('/product/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    conn = sqlite3.connect(connection)
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cursor.execute("UPDATE productos SET nombre = ($n), precio = ($p) WHERE id = ($i)", (nombre, precio, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM productos WHERE id = ($i)", (id,))
    producto = cursor.fetchone()
    conn.close()

    if producto is None:
        return "Producto no encontrado", 404

    return render_template('products/update.html', producto=producto)


@app.route('/product/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    conn = sqlite3.connect(connection)
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute("DELETE FROM productos WHERE id = ($i)", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM productos WHERE id = ($i)", (id,))
    producto = cursor.fetchone()
    conn.close()

    if producto is None:
        return "Producto no encontrado", 404

    return render_template('delete.html', producto=producto)
   
    
@app.route('/products/list')
def list_products():
    conn = sqlite3.connect(connection)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template('products/list.html', productos=productos)   
    
    
# Plantilla

@app.route('/products/list')
def list_products():
    # Connecta amb la base de dades
    connection = sqlite3.connect(connection)
    cursor = connection.cursor()

    # Suposem que tens una taula de productes anomenada "products"
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    # Tanca la connexió amb la base de dades
    connection.close()

    return render_template('list.html', products=products)
   


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


