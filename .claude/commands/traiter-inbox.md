---
description: Trie les screens déposés dans data/inbox/ et ajoute les nouveaux lineups à data/lineups.json
---

Traite la boîte de dépôt `data/inbox/`. Travaille en français. Ne commite et ne pousse RIEN sans validation explicite de l'utilisateur.

## 1. État des lieux
- Lance `git pull` (si ça échoue ou si l'arbre est sale, dis-le et arrête-toi).
- Liste les images (.jpg/.jpeg/.png) dans `data/inbox/<map>/` (dust2, mirage, anubis, ancient, inferno, nuke, cache). Ignore `.gitkeep` et `LISEZ-MOI.txt`. S'il n'y a rien, dis-le et arrête-toi.
- Trie les fichiers de chaque map par date de modification / nom : un lineup = 2 images consécutives, **position puis visée**. Si le nombre est impair ou si l'appariement est douteux, demande à l'utilisateur au lieu de deviner.

## 2. Analyse de chaque paire
Ouvre les deux images avec Read et déduis, en t'inspirant des entrées existantes de `data/lineups.json` (même style, même vocabulaire) :
`map`, `zone` (A / B / Mid…), `side` ("T" ou "CT"), `type` ("smoke" | "molotov" | "flash"), `nom`, `cible`, `depuis` (format « Nom FR (Nom EN) »), `lancer`, `clic`, `position`, `visee`, `temps_vol_s`, `notes`.
- Si les screens contiennent du texte (overlay, HUD, info de lineup), recopie-le fidèlement ; c'est la source prioritaire. Mets le texte d'origine dans `texte_carte`.
- N'invente jamais un chiffre (temps de vol, vitesse, tolérance de visée) : si tu ne le lis pas sur les screens, mets `null` et signale-le.
- `id` = `<map>-<zone>-<slug du nom>` (minuscules, tirets, sans accents) ; doit être unique dans le JSON.
- `images` : `{"position": "<map>/<zone>/<slug>/1_position.jpg", "visee": ".../2_visee.jpg"}` ; `source_screens` : noms de fichiers d'origine ; `getpos`: null ; `strategies`: [].

## 3. Validation (obligatoire)
Présente un tableau récapitulatif (id, type, zone, cible, depuis, doutes) et attends la réponse de l'utilisateur. Corrige selon ses retours. Ne touche à aucun fichier avant son accord.

## 4. Application (après accord)
- Crée `data/screens/<map>/<zone>/<slug>/` et **déplace** (git mv / mv) les deux images, renommées `1_position.jpg` et `2_visee.jpg` (garde l'extension réelle ; si c'est un .png, adapte les chemins dans `images`).
- Ajoute les entrées à `data/lineups.json` avec Python : `json.load` puis `json.dump(..., ensure_ascii=False, indent=2)`, encodage UTF-8, en gardant `version` et l'ordre existant. Ne modifie aucune entrée existante.
- Vérifie : le JSON se recharge, chaque `images.*` pointe vers un fichier existant, aucun `id` en double, et `data/inbox/<map>/` ne contient plus les images traitées (garde `.gitkeep`).

## 5. Fin
Affiche le résumé (lineups ajoutés, fichiers déplacés) puis demande : « Je commite et je pousse ? ». Si oui : `git add data`, commit « Ajout lineups <map> » (+ la ligne Co-Authored-By de la session) et `git push`.
