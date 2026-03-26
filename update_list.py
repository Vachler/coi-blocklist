import requests
import re

def get_coi_data():
    url = "https://www.coi.gov.cz/open-data/rizikove-e-shopy.json"
    domains = set()
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        for eshop in data.get('eshopy', []):
            d = eshop.get('eshop', '').replace('http://', '').replace('https://', '').split('/')[0].strip()
            if d and '.' in d: domains.add(d.lower())
    except: pass
    return domains

def get_soi_data():
    url = "https://www.soi.sk/sk/Rizikove-e-shopy.soi"
    domains = set()
    try:
        r = requests.get(url, timeout=20)
        # Hledáme cokoli, co vypadá jako doména v textu
        found = re.findall(r'([a-z0-9.-]+\.[a-z]{2,10})', r.text.lower())
        for d in found:
            # Ignorujeme vládní a známé weby, které se na stránce SOI vyskytují jako odkazy
            if d and not d.endswith(('soi.sk', 'gov.sk', 'google.com', 'w3.org', 'facebook.com', 'feedburner.com')):
                domains.add(d)
    except: pass
    return domains

MANUAL_DOMAINS = [
    "czjbvers.shop", "botycaterpillar.cz", "zaraeshop.cz", "kamagraobchod.com",
    "riekerobuveshop.sk", "boty-nobull-cz.cz", "praha-couture.com", "eu-notino.shop"
]

if __name__ == "__main__":
    all_domains = get_coi_data() | get_soi_data() | set(MANUAL_DOMAINS)
    # Vyčištění: odstraníme prázdné a příliš krátké nesmysly
    final_list = sorted([f"||{d}^" for d in all_domains if len(d) > 4 and '.' in d])

    if final_list:
        with open("blocklist.txt", "w", encoding="utf-8") as f:
            f.write("! Title: Muj CZ & SK Blocklist\n")
            f.write(f"! Total items: {len(final_list)}\n")
            f.write("! Expires: 1 days\n\n")
            f.write("\n".join(final_list))
