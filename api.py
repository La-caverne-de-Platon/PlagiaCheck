import re
import io
import sys
import json
import asyncio
import argparse
import requests
import nodriver as uc

from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
from urllib.parse import quote
from difflib import SequenceMatcher
from urllib.parse import quote_plus

# fuzzywuzzy
def check_similarity_fuzzy(assignment_text, search_results):
    highest_similarity = 0
    most_similar_result = ""
    
    for result in search_results:
        similarity_ratio = fuzz.ratio(assignment_text, result['content'])
        if similarity_ratio > highest_similarity:
            highest_similarity = similarity_ratio
            most_similar_result = result['url']

    if highest_similarity > 30:  
        return str(highest_similarity) + "%" + most_similar_result
    else:
        return "0"



def extract_google_search_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    search_results = []

    for result in soup.find_all('article', class_='result'):
        title = result.find('h3').get_text(strip=True)
        url = result.find('a', href=True)['href']
        content = result.find('p', class_='content').get_text()
        
        search_result = {
            'title': title,
            'url': url,
            'content': content
        }
        search_results.append(search_result)

    return search_results





async def GoogleSearch(query):
    driver = await uc.start(headless=True)
    url = 'https://searxng.site/searxng/search?q=' + quote(query) + '&language=auto&time_range=&safesearch=2&categories=general'
    tab = await driver.get(url)
    html = await tab.get_content()

    # Close the browser
    await tab.close()
    return html


async def ZeroGPTSearch(query):
    driver = await uc.start(headless=True)
    tab = await driver.get("https://www.zerogpt.com/fr/")
    input_text = query

    textarea = await tab.select("textarea#textArea")
    await textarea.click()
    textarea = await tab.select("textarea#textArea")
    await textarea.click()
    textarea = await tab.select("textarea#textArea")
    await textarea.click()
    await tab.sleep(5)
    textarea = await tab.select("textarea#textArea")
    await textarea.click()
    await textarea.send_keys(input_text)

    detect_button = await tab.select("button.scoreButton")
    await detect_button.click()

    try:
        result_elements = await tab.select("div.final-result")
        # Close the browser
        await tab.close()
        return result_elements
    except Exception as e:
        print("Erreur:", e)


    
    
   


if __name__ == "__main__":
   
    debug_mode = False
    resultIA = 0
    google_result = ""


    if debug_mode:
        input_text = "Le langage est capable de dire aussi bien ce qui existe que ce qui n'existe pas : il me permet aussi bien de décrire un événement qui s'est réellement produit"
    else:
        parser = argparse.ArgumentParser(description="Récupéré le pourcentage de similarité et d'I.A.")
        parser.add_argument("input", type=str, help="Le texte à vérifier")
        args = parser.parse_args()
        input_text = args.input

    #print("Bonjour ! Vérification de l'authenticité de la composition suivante :")
    #print("```")
    #print(input_text)
    #print("```")

    #print("Cherchons sur Google tout d'abord...")
    # GOOGLE SERP
    html_content = asyncio.run(GoogleSearch(input_text))    
    assignment_text = input_text
    search_results = extract_google_search_results(html_content)
    google_results = check_similarity_fuzzy(assignment_text, search_results)
    if(google_results != "0"):
        google_score = google_results.split("%")[0] + "%"
        google_result = google_results.split("%")[1]

        #print(f"[!] Attention : contenu très similaire ({google_score}) trouvé sur Google")
        #print(google_result)
    else:
        #print("Rien de similaire sur Google :-) !")
        #print("Vérifions désormais via ZeroGPT si ce n'est pas un texte généré par I.A. :")
        # ZEROGPT
        old_stdout = sys.stdout # Impossible pour moi de trouver une autre façon de récupérer le contenu Async de tab.Elements ! Une vraie galère
        sys.stdout = buffer = io.StringIO()

        result_texts = asyncio.run(ZeroGPTSearch(input_text))
        rint(result_texts)
        sys.stdout = old_stdout

        resultIA = buffer.getvalue()
        resultIA = resultIA.split("highlights-container")[0]
        resultIA = resultIA.split("header-text text-center")[2]
        resultIA = resultIA.split("%")[0]
        resultIA = resultIA.split('">')[1]
        #print(resultIA + "% de chance que ce texte soit produit par un GPT !")
    

    results_dic = {"google": google_result, "IA": resultIA}
    # Convert dictionary to JSON string
    json_string = json.dumps(results_dic)

    # Print the JSON string
    print(json_string)
    # Define the file path
    file_path = "result.json"

    # Write the JSON string to the file
    with open(file_path, "w") as json_file:
        json_file.write(json_string)
