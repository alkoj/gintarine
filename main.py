import csv
import time
from requests import get
from lxml.html import fromstring

# Nustatome vykdymo laiką
time_limit = 20  # Laikas sekundėmis
start_time = time.time()  # Įsimename pradžios laiką

# Atidarome failą įrašymui CSV formatu
with open("products.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Įrašome CSV antraštes
    writer.writerow(["Product Name", "Product Price", "Product Brand"])

    page_number = 1  # Dabartinio puslapio numeris

    while True:
        # Tikriname, ar laikas nėra pasibaigęs
        if time.time() - start_time > time_limit:
            print("Laiko analizės trukmė pasibaigė.")
            break

        url = f"https://www.gintarine.lt/maistas-ir-papildai-sportininkams?pagenumber={page_number}"
        response = get(url)

        if response.status_code == 200:
            html_content = response.text
            tree = fromstring(html_content)

            # Ištraukite visus produktus
            products = tree.xpath("//div[contains(@class, 'product-item')]")

            if not products:  # Nutraukimas, jei prekės nerastos
                print("Prekės nerastos puslapyje.")
                break

            for product in products:
                product_name = product.xpath(".//input[@name='productName']/@value")
                product_price = product.xpath(".//input[@name='productPrice']/@value")
                product_brand = product.xpath(".//input[@name='productBrand']/@value")

                # Patikrinkite, ar duomenys yra prieš įrašant
                if product_name and product_price and product_brand:
                    writer.writerow([product_name[0], product_price[0], product_brand[0]])

            print(f"Duomenys iš puslapio {page_number} sėkmingai išsaugoti.")
            page_number += 1  # Pereiname į kitą puslapį
        else:
            print(f"Klaida įkeliant puslapį {page_number}: {response.status_code}")
            break

print("Analizė baigta. Duomenys išsaugoti faile products.csv.")