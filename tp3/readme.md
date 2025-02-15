# TD n°3 WANG Mingxuan
## Structure
Deux fichiers:
bucket.py pour **la méthode 1**, cad des buckets équirépartis entre le min et max global.
imbalanced_bucket.py pour **la méthode 2**, `calculation des quantiles`.

En plus, j'ai ajouté dans le fichier bucket.py la création des datas déséquilibrés afin de comparer la performance des deux méthodes.

## How to run
Veuillez taper par exemple `mpirun -n 4 python3 bucket.py` dans le terminal.

## Résultats:

Méthode 1|Méthode 1
-------------------------------------
balanced data|imbalanced data
-------------------------------------
0.000076|0.000320 |
------------------------------
0.000081|0.000058 |
-----------------------------
0.000079|0.000008 |
-------------------------------
0.000074|0.000008 |