from sklearn.model_selection import train_test_split
import seaborn as sns
from matplotlib import pyplot as plt

from sintetic_data import gerar_dados_sinteticos
from utils import classificar, lemmatizer

# Gera dados sintéticos
data = gerar_dados_sinteticos(100, noise=False)

# Classifica a coluna tipo entre melhoria(1) e corretiva(0)
data["Tipo"] = data["Tipo"].apply(classificar)

# Divide os dados em conjuntos de treinamento e teste
df_train, df_test = train_test_split(data, test_size=0.2, random_state=42)

x = df_train['Tipo'].value_counts()

text = 'Implementar sistema de backup no andar térreo'

lemmatizer(text)