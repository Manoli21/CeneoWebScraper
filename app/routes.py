from app import app
from flask import render_template, redirect, url_for, request
import requests
import json
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from app.models.product import Product
from app.utils import get_item



@app.route('/')
def index(name="Hello World"):
    return render_template("index.html.jinja", text=name)

@app.route('/extract/', methods=["POST" , "GET"])
def extract():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        product = Product(product_id)
        product.extract_product().process_stats
        product.save_stats()
        product.save_opinions()
    else:
        return render_template("extract.html.jinja")

@app.route('/products')
def products():
    products = [filename.split(".")[0] for filename in os.listdir("app/opinions")]
    return render_template("products.html.jinja", products=products)

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id):
    product = Product(product_id)
    
    return render_template("product.html.jinja", stats=stats, product_id=product_id, opinions=opinions)