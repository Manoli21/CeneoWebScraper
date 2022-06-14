from bs4 import BeautifulSoup
import requests
import os
import json
import pandas as pd
import numpy as np
from app.utils import get_item
from app.models.opinion import Opinion
from matplotlib import pyplot as plt

class Product:
    def __init__(self, product_id = 0, opinions = [], product_name = "", opinions_count = 0, pros_count = 0, cons_count = 0, average_score = 0):
        self.product_id = product_id
        self.product_name = product_name
        self.opinions = opinions 
        self.opinions_count = opinions_count
        self.pros_count = pros_count
        self.cons_count = cons_count
        self.average_score = average_score
        return self

    def __str__(self):
        return f"opinion_id:{self.opinion_id}<br>" + "<br>".join(f"{key}: {str(getattr(self,key))}" for key in self.compontents.keys())

    def __repr__(self):
        return f"Opinion(opinion_id={self.opinion_id}, " + "<br>".join(f"{key}:{str(getattr(self,key))}" for key in self.compontents.keys()) + ")"

    def to_dict(self):
        return {"opinion_id:self.opinion_id} | {key: getattr(getattr(self,key)" for key in self.compontents.keys()}




    def extract_product(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        response = requests.get(url)
        page = BeautifulSoup(response.text, 'html.parser')
        self.product_name = get_item(page, "h1.product-top__product-info__name")
        while(url):
            response = requests.get(url)
            page = BeautifulSoup(response.text, 'html.parser')
            opinions = page.select("div.js_product-review")
            for opinion in opinions:
                self.opinions.append(Opinion().extract_opinion(opinion))
            try:    
                url = "https://www.ceneo.pl"+get_item(page,"a.pagination__next","href")
            except TypeError:
                url = None


    def opinions_do_df(self):
        opinions = pd.read_json(json.dumps([opinion.to_dict() for opinion in self.opinions]))
        opinions.stars = opinions.stars.map(lambda x: float(x.split("/")[0].replace(",", ".")))
        return opinions

    def process_stats(self):
        self.opinions_count = len(self.opinions_do_df().index)
        self.opinions_count = len(opinions.index),
        self.pros_count = opinions.pros.map(bool).sum(),
        self.cons_count = opinions.cons.map(bool).sum(),
        self.average_score = self.opinions_do_df().stars.mean().round(2)
        return self

    def draw_charts(self):
        recommendation = self.opinions_do_df().recommendation.value_counts(dropna = False).sort_index().reindex(["Nie polecam", "Polecam", None])
        recommendation.plot.pie(
            label="", 
            autopct="%1.1f%%", 
            colors=["crimson", "forestgreen", "lightskyblue"],
            labels=["Nie polecam", "Polecam", "Nie mam zdania"]
        )
        plt.title("Rekomendacja")
        plt.savefig(f"app/static/plots/{product_id}_recommendations.png")
        plt.close()

        stars = self.opinions_do_df().stars.value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
        stars.plot.bar()
        plt.title("Oceny produktu")
        plt.xlabel("Liczba gwiazdek")
        plt.ylabel("Liczba opinii")
        plt.grid(True)
        plt.xticks(rotation=0)
        plt.savefig(f"app/static/plots/{product_id}_stars.png")
        plt.close()



    def save_opinions (self):
        if not os.path.exists("app/opinions"):
            os.makedirs("app/opinions")
        with open(f"app/opinions/{self.product_id}.json", "w", encoding="UTF-8") as jf:
            json.dump(self.to_dict(), jf, indent=4, ensure_ascii=False)

    def save_stats (self):
        if not os.path.exists("app/products"):
            os.makedirs("app/products")
        with open(f"app/opinions/{self.product_id}.json", "w", encoding="UTF-8") as jf:
            json.dump(self.all_opinions, jf, indent=4, ensure_ascii=False)
        return redirect(url_for("product", product_id=product_id))

    def read_from_json(self):
        with open(f"app/products/{self.products_id}.json", "r", encoding="UTF-8") as jf:
            product = json.load(jf)

# Opis produktu, podejścia, walidacja kodu produktu, na lista produktów statystyki, pojedyncza strona żeby się pojawiały opinie, uzupełniamy o autorze
# wiecej punktów, obiektowe podejscie we flasku wtforms dla pobieranie produktów