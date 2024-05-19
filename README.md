# PlagiaCheck
Comment utiliser les nouveaux Crawler spécialisés pour les LLM pour détecter le plagiat

![](https://i.imgur.com/gHve3yV.png)

## Markdowner

Github m'a recommandé le repo ["Markdowner"](https://md.dhr.wtf/), un crawler de données spécialisé dans les LLM. Après quelques usages j'ai vu qu'il pouvait crawl les résultats Google sans problème. Or normalement c'est impossible sans passer directement par Google et payer quelques euros pour pouvoir utiliser la fontionnalité de recherche...

## Taux de similarité

Le script python en exemple prend une [phrase comme argument ici](https://github.com/La-caverne-de-Platon/PlagiaCheck/blob/3cf757d7ed538d00a603c8c4c07bb5de95b3396c/exemple.py#L40) et l'envoie à Google via Markdowner. Ensuite pour chaque ligne dans la réponse, j'utilise [difflib](https://docs.python.org/3/library/difflib.html) qui s'occupe de calculer les déltas et de me donner une valeur de similarité.

### TODO

- [ ] ajouter le modèle de ZeroGPT
