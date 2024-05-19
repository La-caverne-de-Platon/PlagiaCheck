import re
import io
import sys
import asyncio
import nodriver as uc


async def main():
    driver = await uc.start(headless=True)
    tab = await driver.get("https://www.zerogpt.com/fr/")
    input_text = "Peut-on tout dire ? Dans une société fondée sur la liberté d'expression, la question de savoir si l'on peut tout dire suscite des débats passionnés et soulève des enjeux éthiques, moraux et sociaux considérables. Cette interrogation met en balance les principes de liberté individuelle et les limites nécessaires pour préserver l'ordre, la sécurité et le respect mutuel au sein de la société. Ainsi, aborder cette question exige une analyse approfondie des différents aspects impliqués. D'une part, défendre le droit de tout dire revient à soutenir la liberté d'expression comme un pilier fondamental de la démocratie. En permettant à chacun d'exprimer ses opinions, même les plus controversées, la société favorise le débat d'idées et la diversité des perspectives. Cette liberté constitue également un contrepoids essentiel contre les abus de pouvoir et les injustices, car elle permet de dénoncer les atteintes aux droits humains et les dysfonctionnements de la société. Cependant, cette liberté absolue trouve ses limites dans le respect des droits et de la dignité d'autrui, ainsi que dans la préservation de l'ordre public. En effet, certaines formes d'expression, telles que la diffamation, l'incitation à la haine ou à la violence, peuvent causer des préjudices graves et compromettre la cohésion sociale. De même, les discours qui portent atteinte à la vie privée, à l'intégrité physique ou psychologique des individus ne peuvent être tolérés au nom de la liberté d'expression. Par ailleurs, la liberté d'expression implique la responsabilité de chacun quant aux conséquences de ses paroles. Si l'on peut avoir le droit de dire certaines choses, il est également crucial de prendre en compte l'impact de nos propos sur autrui. Ainsi, la liberté d'expression ne saurait être un prétexte pour justifier la propagation de fausses informations, la stigmatisation de groupes sociaux ou toute forme de discours discriminatoire. En définitive, la question de savoir si l'on peut tout dire ne peut être tranchée de manière catégorique. La liberté d'expression est un principe fondamental, mais elle doit être exercée avec discernement et responsabilité. Les sociétés démocratiques doivent trouver un équilibre délicat entre la protection des droits individuels et la préservation de l'ordre et de la cohésion sociale. Cela nécessite non seulement des lois et des régulations adéquates, mais aussi une éducation citoyenne favorisant le respect mutuel, la tolérance et la compréhension des différences. En conclusion, si la liberté d'expression constitue un droit essentiel, elle n'est pas absolue et doit"

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
        return result_elements
    except Exception as e:
        print("Erreur:", e)

    await driver.close()

    
    
   
old_stdout = sys.stdout # Impossible pour moi de trouver une autre façon de récupérer le contenu Async de tab.Elements ! Une vraie galère
sys.stdout = buffer = io.StringIO()

result_texts = asyncio.run(main())
print(result_texts)
sys.stdout = old_stdout

result = buffer.getvalue()
result = result.split("highlights-container")[0]
result = result.split("header-text text-center")[2]
result = result.split("%")[0]
result = result.split('">')[1]
print(result + "% de chance que ce texte soit produit par un GPT !")
