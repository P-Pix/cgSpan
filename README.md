# cgSpan
Ce projet est une version corrigée de l'algorithme cgSpan de Philippe FOURNIER-VIGER qui ne fonctionne pas correctement.

## Utilisation

Pour utiliser cette librairie, il faut réaliser le setup puis suivre l'exécution.

### Setup

Afin de faire fonctionner correctement le projet, il est nécessaire de télécharger la libraire [`spmf.jar`](https://www.philippe-fournier-viger.com/spmf/spmf.zip) de Philippe FOURNIER-VIGER et de télécharger la librairie. [`spmf.py`](https://github.com/LoLei/spmf-py)
via la commande suivante :

```shell
pip install spmf
```

ou exécuter la commande suivante pour tout réaliser :

```shell
sh setup.sh
```

### Éxécution

Pour exécuter la fonction, il faut avoir une liste de graphes [NetworkX](https://networkx.org/) et importer la fonction comme tel :

```python
from cgSpan.src.cgSpan import cgSpan

# retourne la liste des sous-graphes fréquents fermés avec leur fréquence de parution

freq_min = 0.2
graphes = cgSpan(liste_graphes, freq_min)
```

## Citation

Si vous venez à utiliser cette librairie merci de la citer en référence :

```txt
Guillaume LEMONNIER, https://github.com/P-Pix/cgSpan (2025)
```

## Références

[SPMF](https://www.philippe-fournier-viger.com/spmf/)