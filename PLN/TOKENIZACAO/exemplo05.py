# 1. Importar a biblioteca NLTK
import nltk

# 2. Definir o texto a ser tokenizado
texto = "Paulo Freire disse que quando a educação não é libertadora, o sonho do oprimido é ser o opressor. Em tempos de minorias fazendo campanha para candidato que despreza seus direitos e necessidades, fica claro que nunca tivemos uma educação de fato libertadora. ;( #DiaDosProfessores #EducacaoLibertadora @PauloFreireOficial"

# 3. Definir o tokenizador de tweets
tokenizador = nltk.TweetTokenizer()

# 4. Tokenizar o texto
# Array que vai receber o tweet tokenizado
tweet = tokenizador.tokenize(texto)

print(tweet)