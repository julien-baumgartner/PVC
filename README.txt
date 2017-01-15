L'algorithme alterne entre sélection, croisement et mutation

La mutation est de plus en plus grande en fonction du temps écoulé, car il faudra plus de chance pour tomber sur une meilleure solution
Le croisement que nous utilisons est la méthode du random qui à partir de N echantillon, génere un certain nombre d'échantillon supplémentaire en prenant des combinaisons uniques et aléatoires
Une combinaison n'implique qu'un seul nouvel échantillon mais l'inverse de la combinaison n'est pas automatiquement repris
La selection se fait par rapport à la distance total du chemin et est proportionnelle au nombre de solution

Plus il y a de villes, plus le nombre de solutions calculées simultanément est petit car sinon les calculs sont trop lent
