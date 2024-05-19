import requests
from difflib import SequenceMatcher
from urllib.parse import quote_plus
from urllib.parse import quote

# Fonction pour créer un délai aléatoire
def random_delay():
    time.sleep(random.uniform(1, 5))

def get_search_results(query):
    query = quote(query)
    url = 'https://md.dhr.wtf/?url=https://www.google.com/search?q=' + query
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve data:", response.status_code)
    return ""

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def main(input_text):
    # Encodage de l'input_text pour être utilisé dans une URL
    encoded_text = quote_plus(input_text)
    search_results = get_search_results(encoded_text)

    bestsim = 0
    
    for line in search_results.split('\n'):
        sim = similarity(input_text, line)
        if(sim > 0.5):
            if(sim > bestsim):
                bestsim = sim
            print(f"Similarity between '{input_text}' and '{line}': {sim}")
    
    return bestsim

if __name__ == "__main__":
    input_text = "À l'ère d'Internet et de la société de communication, c'est un droit qui s'exerce à une échelle inédite. Mais peut‑on tout dire ? Quelles sont les limites de la"
    similarity_score = main(input_text)
    print(f"Highest similarity score: {similarity_score:.2f}")
