import bentoml
from sklearn import svm
from sklearn import datasets

# 1. Načítanie dát
iris = datasets.load_iris()
X, y = iris.data, iris.target

# 2. Tréning modelu (jednoduchý Support Vector Machine)
clf = svm.SVC(gamma='scale')
clf.fit(X, y)

# 3. Uloženie modelu do BentoML Model Store
# 'iris_clf' je názov, pod ktorým model nájdeš neskôr
# BentoML vezme tie čisté váhy (binárny súbor) a uloží ich do špeciálneho priečinka 
# vo tvojom počítači (zvyčajne v ~/bentoml/models/). 
# Každá verzia má svoj unikátny tag (napr. housing_regressor:abc123xyz).
saved_model = bentoml.sklearn.save_model("iris_clf", clf)

print(f"Model bol úspešne uložený: {saved_model}")