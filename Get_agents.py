import requests
import time
import csv

URL_GEOJSON = "https://api.meilleursbiens.com/api/v1/mbportail/agents/geojson.json"

def get_agents():
    response = requests.get(URL_GEOJSON)
    data = response.json()
    return data["features"]

def get_all_pages(slug, status=None):
    tous_les_biens = []
    page = 1
    last_data = None

    while True:
        if status:
            url = f"https://api.meilleursbiens.com/api/v2/mbportail/biens/agent/{slug}?page={page}&status={status}"
        else:
            url = f"https://api.meilleursbiens.com/api/v2/mbportail/biens/agent/{slug}?page={page}"

        try:
            response = requests.get(url, timeout=10)
            data = response.json()
        except Exception as e:
            print(f"  Erreur réseau pour {slug} : {e}")
            break

        if not isinstance(data.get("data"), dict):
            print(f"  Structure inattendue pour {slug}, on passe.")
            break

        biens_page = data["data"]["data"]
        tous_les_biens.extend(biens_page)
        last_data = data

        last_page = data["data"]["last_page"]
        if page >= last_page:
            break

        page += 1
        time.sleep(0.3)

    return tous_les_biens, last_data

def calculer_stats(slug):
    biens_actifs, last_data = get_all_pages(slug, status=1)
    biens_vendus, _ = get_all_pages(slug, status=3)

    nb_mandates = len(biens_actifs)
    nb_sales = len(biens_vendus)

    prix = [b["price_public"] for b in biens_actifs if b.get("price_public")]
    avg_price = int(sum(prix) / len(prix)) if prix else 0

    return nb_mandates, avg_price, nb_sales, last_data

def extraire_telephone(slug):
    try:
        url = f"https://api.meilleursbiens.com/api/v1/mbportail/agent/phone/{slug}"
        response = requests.get(url, timeout=10)
        data = response.json()
        telephone = data.get("data", {}).get("phone", "") or ""

        if telephone and not telephone.startswith("+"):
            telephone = "+" + telephone

        return telephone
    except:
        return ""

def extraire_linkedin(data):
    try:
        return data["data"]["data"][0]["user"]["profile"]["link_linkedin"] or ""
    except:
        return ""

# --- PROGRAMME PRINCIPAL ---
agents = get_agents()
print(f"Nombre d'agents à traiter : {len(agents)}")

with open("agents.csv", "w", newline="", encoding="utf-8-sig") as fichier_csv:

    colonnes = ["first_name", "last_name", "postal_code", "city",
                "phone_number", "email", "nb_mandates", "avg_mandate_price",
                "nb_sales", "linkedin_url"]

    writer = csv.DictWriter(fichier_csv, fieldnames=colonnes)
    writer.writeheader()

    for i, agent in enumerate(agents):
        user = agent["properties"]["user"]
        profile = user["profile"]

        first_name = profile.get("first_name", "")
        last_name = profile.get("name", "")
        email = user.get("emailPro", "")
        postal_code = user.get("postalCode", "")
        city = user.get("city", "")
        slug = user.get("slug", "")

        print(f"[{i+1}/{len(agents)}] Traitement de {first_name} {last_name}...")

        nb_mandates, avg_price, nb_sales, data = calculer_stats(slug)

        if data is None:
            telephone = ""
            linkedin = ""
        else:
            telephone = extraire_telephone(slug)
            linkedin = extraire_linkedin(data)

        writer.writerow({
            "first_name": first_name,
            "last_name": last_name,
            "postal_code": postal_code,
            "city": city,
            "phone_number": telephone,
            "email": email,
            "nb_mandates": nb_mandates,
            "avg_mandate_price": avg_price,
            "nb_sales": nb_sales,
            "linkedin_url": linkedin
        })

        time.sleep(0.5)

print(" Fichier agents.csv créé")
