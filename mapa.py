import pandas as pd

mapa_poligono = pd.read_csv('data_master/table_contiguity_queen.csv', sep=',')

# Crie uma lista de todos os municípios únicos
municipios = sorted(set(mapa_poligono['municipio_1'].unique()) | set(mapa_poligono['municipio_2'].unique()))

# Crie um dicionário para mapear índices para nomes de municípios
municipio_index = {municipio: i for i, municipio in enumerate(municipios)}

# Crie uma matriz de zeros para todos os municípios
n = len(municipios)
matrix = [[0] * n for _ in range(n)]

# Preencha a matriz com 1 onde os municípios se tocam
for _, row in mapa_poligono.iterrows():
    municipio1 = row['municipio_1']
    municipio2 = row['municipio_2']
    i = municipios.index(municipio1)
    j = municipios.index(municipio2)
    matrix[i][j] = 1
    matrix[j][i] = 1

# Converta a matriz em um DataFrame
matrix_df = pd.DataFrame(matrix, columns=municipios, index=municipios)

# Salve a matriz em um arquivo CSV
matrix_df.to_csv('output_geral/matriz_toque_geral.csv', index=True, header=True)

# Exiba a matriz ou faça o que for necessário com ela
print('Matriz Geral:')
print(matrix_df)