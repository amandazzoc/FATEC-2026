import nltk

texto = "No meio do caminho tinha uma pedra tinha uma pedra no meio do caminho tinha uma pedra no meio do caminho tinha uma pedra. Nunca me esquecerei desse acontecimento na vida de minhas retinas tão fatigadas. Nunca me esquecerei que no meio do caminho tinha uma pedra tinha uma pedra no meio do caminho no meio do caminho tinha uma pedra."
 
palavras = []

palavras = nltk.word_tokenize(texto.lower())

tags = nltk.pos_tag(palavras)

print(tags)

# Possívels rótulos

# NN: Nome/Substantivo no singular
# NNS: Nome/Substantivo no plural
# VB: Verbo no infinitivo
# VBD: Verbo no passado
# VBG: Verbo no gerúndio
# VBP: Verbo no presente
# DT: Determinante
# JJ: Adjetivo
# FW: Palavra estrangeira
# IN: Palavra de negação
# PRP: Pronome pessoal
# SYM: Símbolo
# CD: Número cardinal