import nltk

texto="No meio do caminho tinha uma pedra tinha uma pedra no meio do caminho tinha uma pedra no meio do caminho tinha uma pedra. Nunca me esquecerei desse acontecimento na vida de minhas retinas tão fatigadas. Nunca me esquecerei que no meio do caminho tinha uma pedra tinha uma pedra no meio do caminho no meio do caminho tinha uma pedra."

# Diferença entre sent_tokenize e word_tokenize é que sent_tokenize separa o texto em frases e word_tokenize separa o texto em palavras.
palavras = nltk.word_tokenize(texto)

print(palavras)
