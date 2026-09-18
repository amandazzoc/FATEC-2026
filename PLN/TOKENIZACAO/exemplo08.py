# palavras que são removidas, como artigo, advérbio, preposição
 
import nltk
 
texto = "No meio do caminho tinha uma pedra tinha uma pedra no meio do caminho tinha uma pedra no meio do caminho tinha uma pedra. Nunca me esquecerei desse acontecimento na vida de minhas retinas tão fatigadas. Nunca me esquecerei que no meio do caminho tinha uma pedra tinha uma pedra no meio do caminho no meio do caminho tinha uma pedra."

vocabulario = []
 
palavras = nltk.word_tokenize(texto.lower())
 
# stop word removidos da base do nltk, mas eu posso criar o meu próprio array de stop words, caso queira remover palavras específicas do meu texto
stop_words = nltk.corpus.stopwords.words('portuguese')
 
# pra cada palavra no array, tenho que comparar com as stop words, se a palavra estiver no array de stop words, eu removo do array de palavras
# um for dentro do outro fica ruim para textos muito grandes, até na integradora por mais que sejam textos pequenos
for palavra in palavras:
    if not(palavra in stop_words):
        vocabulario.append(palavra)
 
print("--- STOP WORDS (PADRÃO DO NLTK) ---")
print(stop_words)
