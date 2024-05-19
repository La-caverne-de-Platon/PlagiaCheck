# PlagiaCheck
Un script python qui permet de détecter le plagiat en utilisant Google et la détection d'I.A. via ZeroGPT !

## L'utiliser localement

```bash
python api.py "Être heureux : Bonheur signifie bon heur, heur étant dérivé du latin augurium, qui signifie « augure, « chance ». C’est quelque chose qui nous échoit, qui ne dépend pas de nous. La définition académique du bonheur est « aspiration commune à tous, état durable de satisfaction et de plénitude ». Bon, dans bonheur suggère l’idée d’un bien. Mais s’agit-il de l’agréable ou du bien moral ?"
```

résultat : 

```bash
{"google": "https://www.studocu.com/fr/document/ecole-internationale-bilingue-section-etoile/philosophie/sequence-2-la-liberte-conduit-elle-au-bonheur/90421849", "IA": 0}
```

## L'utiliser via l'API

Pour faciliter tout le monde j'héberge le fichier python sur mon VPS derrière mon site à cette addresse : [https://lacavernedeplaton.fr/api/science.php](https://lacavernedeplaton.fr/api/science.php)

## Documentation de l'API 

### Envoyer des données
Pour envoyer des données textuelles pour vérification de plagiat, vous pouvez effectuer une requête POST vers le point d'accès `/science.php` avec les données textuelles dans le paramètre `p`.

```bash
curl -X POST https://lacavernedeplaton.fr/api/science.php -d 'p=Lorem%20ipsum%20dolor%20sit%20amet'
```

Résultat : 

```bash
456
```

### Récupérer les résultats
Une fois que les données sont soumises avec succès, vous recevrez un identifiant de tâche. Vous pouvez ensuite utiliser cet identifiant pour récupérer les résultats de vérification de plagiat.

```bash
curl -X GET https://lacavernedeplaton.fr/api/science.php?id=123456
```

Résultat :

résultat : 

```bash
{"google": "https://www.studocu.com/fr/document/ecole-internationale-bilingue-section-etoile/philosophie/sequence-2-la-liberte-conduit-elle-au-bonheur/90421849", "IA": 0}
```

### Gestion des erreurs
- Si aucune donnée n'est fournie pour la vérification du plagiat, l'API renvoie un formulaire HTML pour soumettre des données.
- Si un identifiant de tâche invalide est fourni pour récupérer les résultats, l'API renvoie une réponse vide.
