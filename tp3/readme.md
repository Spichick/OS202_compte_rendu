# TD n°3 WANG Mingxuan
## Structure
Deux fichiers:
bucket.py pour **la méthode 1**, cad des buckets équirépartis entre le min et max global.
imbalanced_bucket.py pour **la méthode 2**, `calculation des quantiles`.

En plus, j'ai ajouté dans le fichier bucket.py la création des datas déséquilibrés afin de comparer la performance des deux méthodes.

## How to run
Veuillez taper par exemple `mpirun -n 4 python3 bucket.py` dans le terminal.

## Résultats

|| Méthode 1 | Méthode 1 | Méthode 2 | Méthode 2 |
|--|--------------------------|----------------------------|--------------------------|----------------------------|
|--| balanced data            | imbalanced data            | balanced data            | imbalanced data            |
|Process 0| 0.000076                 | 0.000320                   | 0.000076                 | 0.000078                   |
|Process 1| 0.000081                 | 0.000058                   | 0.000077                 | 0.000077                   |
|Process 2| 0.000079                 | 0.000008                   | 0.000077                 | 0.000076                   |
|Process 3| 0.000074                 | 0.000008                   | 0.000076                 | 0.000076                   |
(Unité : s)

| Random Data Type  | 0.0 - 0.1 | 0.1 - 0.2 | 0.2 - 0.3 | 0.3 - 0.4 | 0.4 - 0.5 | 0.5 - 0.6 | 0.6 - 0.7 | 0.7 - 0.8 | 0.8 - 0.9 | 0.9 - 1.0 |
|------------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| Balanced Data| 471       | 516       | 533       | 517       | 467       | 476       | 523       | 490       | 491       | 516       |
| Imbalanced Data| 4831     | 63        | 25        | 13        | 15        | 12        | 14        | 9         | 7         | 11        |
