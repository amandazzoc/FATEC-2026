import pandas as pd

import re
# Trabalha com expressões regulares, limpar dados e remover caracteres indesejados

import unicodedata
# Tratamento de caracteres Unicode, remover acentos e ajudar na padronização de textos.

from pathlib import Path
# Permite localizar o arquivo CVS de forma mais segura, independetemente da pasta em que o terminal foi aberto.

from sklearn.preprocessing import MinMaxScaler
# Ferramenta de Normalização, transformar valores numéricos para uma escala entre 0 e 1

from sklearn.preprocessing import RobustScaler
# Ferramenta de transformação mais resistente a outliners, utiliza a medina e os quartis, em vez da média e do desvio padrão

from sklearn.model_selection import train_test_split
# Função utilizada para dividir uma base de dados em conjunto de treinamento e conjunto de teste. É importante para avaliar modelos de Machine Learning utilizando dados que não participam do treinamento.

# Configuração
# Localizar o CSV na mesma pasta do programa
arquivo = Path(__file__).resolve().parent / 'base_ecommerce_brasil_2026_suja.csv'

# Carregar a base externa
df=pd.read_csv(arquivo, sep=';', encoding='utf-8')

# Função auxiliar: remove acentos, pontuação e diferenças de maiusculo/minusculo
def padronizar_texto(valor):
    if pd.isna(valor):
        return valor
    
    valor = str(valor).strip().upper()  # Remove espaços em branco e converte para maiúsculas
    valor = ''.join(
        letra for letra in unicodedata.normalize('NFKC', valor)
        if not unicodedata.combining(letra)
    )
    
    valor = re.sub(r'[^A-Z0-9]', '', valor)
    return re.sub(r'\s+', ' ', valor)  # Remove espaços extras

# Conhecer a base sem alterar nada.
print('Linhas Recebidas: ', len(df))
print('Duplicados Exatos: ', df.duplicated().sum())
print('IDs de pedido repetidos: ', df.duplicated('id_pedido').sum())
print('Pedidos únicos: ', df['id_pedido'].nunique())

# Remover apenas as linhas totalmente iguais
limpo = df.drop_duplicates().copy()

# Padronizar campos textuais importantes.
limpo['nome_cliente'] = limpo['nome_cliente'].str.strip().str.title()
limpo['email'] = limpo['email'].str.strip().str.lower()
limpo['telefone'] = limpo['telefone'].str.replace(r'\D', '', regex=True)  # Remove caracteres não numéricos
limpo['data_pedido'] = pd.to_datetime(limpo['data_pedido'], errors='coerce', dayfirst=True, format='mixed').dt.strftime('%Y-%m-%d')  # Padroniza para o formato AAAA-MM-DD

# Estados escritos por extenso serão convertidos para suas siglas
mapa_uf = {
    'ACRE': 'AC',
    'ALAGOAS': 'AL',
    'AMAZONAS': 'AM',
    'AMAPÁ': 'AP',
    'BAHIA': 'BA',
    'CEARÁ': 'CE',
    'DISTRITO FEDERAL': 'DF',
    'ESPÍRITO SANTO': 'ES',
    'GOIÁS': 'GO',
    'MARANHÃO': 'MA',
    'MINAS GERAIS': 'MG',
    'MATO GROSSO DO SUL': 'MS',
    'MATO GROSSO': 'MT',
    'PARÁ': 'PA',
    'PARAÍBA': 'PB',
    'PERNAMBUCO': 'PE',
    'PIAUÍ': 'PI',
    'PARANÁ': 'PR',
    'RIO DE JANEIRO': 'RJ',
    'RIO GRANDE DO NORTE': 'RN',
    'RONDÔNIA': 'RO',
    'RORAIMA': 'RR',
    'RIO GRANDE DO SUL': 'RS',
    'SANTA CATARINA': 'SC',
    'SERGIPE': 'SE',
    'SÃO PAULO': 'SP',
    'TOCANTINS': 'TO'
}

limpo['estado'] = limpo['estado'].map(padronizar_texto).replace(mapa_uf)

# Categorias diferentes que significam a mesma coisa recebem um unico padrão
limpo['forma_pagamento'] = limpo['forma_pagamento'].map(padronizar_texto).replace({
    'PAGAMENTO INSTANTANEO': 'PIX',
    'CARTAOCREDITO': 'CARTAO_CREDITO',
    'CARTAO CREDITO': 'CARTAO_CREDITO',
    'CARTAODEBITO': 'CARTAO_DEBITO',
    'CARTAO DEBITO': 'CARTAO_DEBITO',
    'DEBITO': 'CARTAO_DEBITO',
    'BOLETO BANCARIO': 'BOLETO',
    'CARTEIRADIGITAL': 'CARTEIRA_DIGITAL',
    'WALLET': 'CARTEIRA_DIGITAL',
})

limpo['canal_venda'] = (
    limpo['canal_venda'].map(padronizar_texto).replace({
        'APLICATIVO': 'APP',
        'WEB': 'SITE',
        'MARKET PLACE': 'MARKETPLACE',
        'LOJAFISICA': 'LOJA_FISICA',
        'LOJA FISICA': 'LOJA_FISICA',
        'PDV': 'LOJA_FISICA',
    })
)

limpo['dispositivo'] = limpo['dispositivo'].map(padronizar_texto)
limpo['categoria_produto'] = limpo['categoria_produto'].map(padronizar_texto)

# Após padronizar, registros antes "diferentes" podem se tornar iguais
print('Duplicados revelados após padronização: ', limpo.duplicated().sum())

# Remover essas duplicidade
limpo = limpo.drop_duplicates().copy()
print('Linhas após padronização: ', len(limpo))
print('Estados após padronização: ', limpo['estado'].nunique())
print('Formas de pagamento: ', limpo['forma_pagamento'].nunique())
print('Canais de venda: ', limpo['canal_venda'].nunique())

# Padronização e Normalização
variaveis = ['idade_cliente', 'renda_mensal', 'valor_total']

# Mostra como idade, renda e valor de compra possuem escalar muito diferentes
print('\nEscala Original:')
print(limpo[variaveis].agg(['min', 'max', 'mean']).round(2))

# Min - Max transforma cada atributo para o intervalo de 0 a 1
limpo[['idade_minmax', 'renda_minmax', 'valor_minmax']] = (MinMaxScaler().fit_transform(limpo[variaveis]))

# Z-score deixar a média proxima a 0 e o desvio padrão proximo a 1
limpo[['idade_z', 'renda_z', 'valor_z']] = (StandardScaler().fit_transform(limpo[variaveis]))

# RobustScaler uma a mediana e quarts, sendo útil quando existem outliers
limpo['renda_robusta'] = (RobustScaler().fit_transform(limpo[['renda_mensal']]).ravel())

print('\nExemplo das transformações:')
print(
    limpo[['idade_cliente', 'idade_minmax', 'idade_z', 'renda_mensal', 'renda_minmax', 'renda_z', 'renda_robusta']].head(5).round(3).to_string(index=False)
)

# Discritização e Binarização
limpo['faixa_etaria'] = pd.cut( #pd.cut(): divide os valores em intervalos
    limpo['idade_cliente'], # coluna com a idade de cada cliente
    bins=[17,24,34,44,54,64,120], # define os limites das faixas
    labels=['18-24', '25-34', '35-44', '45-54', '55-64', '65+'] # dá um nome para cada faixa
)

# QCUT: divide o valor das compras em quatro grupos com quantidade semelhantes

limpo['faixa_cliente'] = pd.qcut( #divide os dados em quantis, tentando colocar aproximadamente a mesma quantidade de clientes em cada grupo.
    limpo['valor_total'], # coluna com o valor total das compras
    q=4, # divide em 4 grupos
    labels=['Baixo', 'Médio-baix', 'Médio-alto', 'Alto'] # dá um nome para cada grupo
)

# Binarização: acima de R$1.000 recebe 1; caso abaixo, recebe 0