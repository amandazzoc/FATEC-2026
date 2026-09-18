# Dataset Iris
# Utilizado para demonstrar, passo a passo como um algoritmo de Machine Learning pode aprender padrões e classificar flores de 3 especies

# Importando biblioteca
import pandas as pd
import matplotlib.pyplot as plt # Cria gráficos
from sklearn.datasets import load_iris # Dataset nativo
from sklearn.tree import DecisionTreeClassifier # Árvore de Decisão
from sklearn.tree import plot_tree # Desenha a árvore de decisão

# Métricas utilizadas para avaliar o modelo
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report

# 2 Carregamento do dataset Iris
iris = load_iris()
print('='*50)
print('Dataset Iris')
print('='*50)
print('Dataset Iris carregado com sucesso!')

# 3 Conhecendo o dataset
# Quantidade de registros
print('\nQuantidade de registros existentes:')
print(len(iris.data))

# Nome das características
print('\nCaracterísticas utilizadas para analisar cada flor:')
for características in iris.feature_names:
    print('-', características)
    
# Nome das especies
print('\nEspécies Existentes:')
for especie in iris.target_names:
    print('-', especie)