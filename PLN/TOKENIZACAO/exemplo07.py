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

frases_tokenizadas = []
palavras_tokenizadas = []
palavras_unicas = []

for texto in avaliacao:
    frases = nltk.sent_tokenize(texto)
    for frase in frases:
        frases_tokenizadas.append(frase)

print(frases_tokenizadas)
print("Quantidade de frases tokenizadas: ", len(frases_tokenizadas))

for texto in avaliacao:
    palavras = nltk.word_tokenize(texto)
    for palavra in palavras:
        palavras_tokenizadas.append(palavra)

print(palavras_tokenizadas)
print("Quantidade de palavras tokenizadas: ", len(palavras_tokenizadas))

