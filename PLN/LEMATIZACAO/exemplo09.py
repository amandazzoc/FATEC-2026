import nltk

texto = "No meio do caminho tinha uma pedra tinha uma pedra no meio do caminho tinha uma pedra no meio do caminho tinha uma pedra. Nunca me esquecerei desse acontecimento na vida de minhas retinas tão fatigadas. Nunca me esquecerei que no meio do caminho tinha uma pedra tinha uma pedra no meio do caminho no meio do caminho tinha uma pedra."

palavras = []

palavras = nltk.word_tokenize(texto.lower())

lematizador = nltk.stem.WordNetLemmatizer()

lemas = []

for palavra in palavras:
    lemas.append(lematizador.lemmatize(palavra))

print(lemas)