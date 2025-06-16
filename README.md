# cgSpan
Ce projet est une version corriger de l'algorithme cgSpan de Philippe FOURNIER-VIGER qui ne fonctionne pas correctement.

## Utilisation

Pour utiliser cette librairie il faut réaliser le setup puis suivre l'éxécution.

### Setup

Afin de faire focntionner correctement le projet, il est nécéssaire de télécharger la libraire [`spmf.jar`](https://www.philippe-fournier-viger.com/spmf/spmf.zip) de Philippe FOURNIER-VIGER et de télécharger la librairie [`spmf.py`](https://github.com/LoLei/spmf-py)
via la commande suivante :

```shell
pip install spmf
```

ou éxécuter la commande suivante pour tout réaliser :

```shell
sh setup.sh
```

### Éxécution

Pour éxécuter la fonction il faut avoir une liste de graphes [NetworkX](https://networkx.org/) et importer la fonction comme tel :

```python
from cgSpan.src.cgSpan import cgSpan

# retourne liste des sous graphes fréquents fermés avec leurs fréquence de parrution

graphes = cgSpan(liste_graphes)
```

## Citation

Si vous venez à utiliser cette librairie merci de la citer en référence :

```txt
Guillaume LEMONNIER, https://github.com/P-Pix/cgSpan (2025)
```

## Références

[SPMF](https://www.philippe-fournier-viger.com/spmf/)