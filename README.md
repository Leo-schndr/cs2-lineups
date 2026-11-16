# Lineups CS2

Appli locale pour afficher et réviser ses lineups (smokes, molos, flashs) sur un second écran.

## Lancer
```
pip install -r requirements.txt
python app.py
```
Ou double-clic sur `Lancer.bat`. L'appli s'ouvre sur http://127.0.0.1:5000.

## Données
- `data/lineups.json` : la base des stuffs (modifiable depuis l'appli, bouton « Modifier »)
- `data/screens/<map>/<zone>/<stuff>/` : screens de position et de visée
