import nltk

avaliacao = [
    "Amei e simplesmente lindo já uso dessa marca e tenho preferência por ter problema na coluna e ser indicado pelo ortopedista para minha atividades físicas e no dia a dia!.",
    "O tênis é de boa qualidade, compre, confortável e bonito, muito bom para caminhadas e corridas.",
    "O tênis mais perfeito do mundo, só gosto dessa marca e esse superou minhas expectativas, parece que estou descalça com tanto conforto… eu amei. Pedi meu numero mesmo que eu calço que é 35.",
    "Adoro a asics, tenis extremamente confortáveis. Apenas sempre busco adquirir com reforço na frente, pois tenho o pé largo e rasgo as laterais com facilidade.",
    "Achei pelo preço que era original, mas não é. Bem mais inferior. Só não devolvi pq precisava no dia, mas fiquei decepcionada. Usei e não tem a qualidade do original.",
    "Muito bonito e de qualidade porém eu achei que o 38 ia servir mas ficou pegando um pouco no dedão do pé.",
    "A costura dele na frente não é tão boa, infelizmente eu tenho um igualzinho só muda a cor, mas descosturou em menos de um ano, eu queria muito outro que comprei da mesma marca.",
    "Gastei, confortável e bonito. Mas pelo preço acho que o tecido da frente deveria ser reforçada. O meu rasgou muito rápido.",
    "O tênis é super escorregadio, não parece original, muito diferente do que comprei na loja.",
    "Um pouco duro e pesado.",
    "Tenis extremamente duro, desconfortável.",
    "Achei que não é original. A qualidade do que já possuo é diferente.",
    "Muito inferior, pelo valor; furou nos os dois pés, bem no dedinho. 1 mês de usou.",
    "Não ficou confortável, é meu número, mas parece que ficou pequeno. Eu queria pra andar o dia inteiro, mas com tempo acaba machucando.",
    "O tênis da asics é lindo, mas é muito duro. Não dá para ficar com ele por muito tempo porque machuca o pé. Bonito sim, confortável não.",
    "Achei ele duro. Tenho outros na mesma faixa de preço que são mais macios.",
    "Lamentável. Dois meses de caminhada leve, já furou o tecido. Da pra desconfiar da autenticidade. Baixa qualidade para um asics. Tá mais pra xingling. Não recomendo!!!!!.",
    "Produto ruim, não tem boa qualidade com pouco tempo de uso, sem nem ter sido lavado já está danificando o tecido. Estou contrariada, não recomendo.",
    "Produto nao é original. Nao fica macio no pé. Por isso o custo benefício é menor. Eu preciso de um tenis macio, confortável. Mas esteticamente é bonito.",
    "Nem um pouco macio. Nao gostei, me arrependi de ter pago tão caro num produto que não é nada confortável."
]

# 1. Tokenização de frases
frases_tokenizadas = []
for texto in avaliacao:
    frases = nltk.sent_tokenize(texto)
    for frase in frases:
        frases_tokenizadas.append(frase)

print("1. Quantidade de frases tokenizadas:", len(frases_tokenizadas))
print("Frases tokenizadas:")
for i, frase in enumerate(frases_tokenizadas, start=1):
    print(f"{i}. {frase}")

print("\n---\n")

# 2. Tokenização de palavras
palavras_tokenizadas = []
for frase in frases_tokenizadas:
    palavras = nltk.word_tokenize(frase.lower())
    for palavra in palavras:
        palavras_tokenizadas.append(palavra)

print("2. Total de palavras tokenizadas:", len(palavras_tokenizadas))
print("Palavras tokenizadas:")
for i, palavra in enumerate(palavras_tokenizadas, start=1):
    print(f"{i}. {palavra}")

print("\n---\n")

# 3. Obtenção do Vocabulário Único
vocabulario_unico = sorted(list(set(palavras_tokenizadas)))

print("3. Quantidade de palavras únicas no vocabulário:", len(vocabulario_unico))
print("Vocabulário único:")
for i, palavra in enumerate(vocabulario_unico, start=1):
    print(f"{i}. {palavra}")
    
print("\n---\n")

# 4. Remoção de Stop Words e Pontuação
stop_words = set(nltk.corpus.stopwords.words('portuguese'))

palavras_sem_stopwords = [
    palavra for palavra in vocabulario_unico 
    if palavra.isalnum() and palavra not in stop_words
]

print("4. Palavras restantes após remover stop words:", len(palavras_sem_stopwords))
print("Palavras sem stop words:")
for i, palavra in enumerate(palavras_sem_stopwords, start=1):
    print(f"{i}. {palavra}")

print("\n---\n")

# 5. Lematização com WordNet
lematizador = nltk.stem.WordNetLemmatizer()

lemas = []
for palavra in palavras_sem_stopwords:
    lemas.append(lematizador.lemmatize(palavra))

print("5. Quantidade de lemas:", len(lemas))
print("\nLemas gerados:")
print(list(lemas)[:15])