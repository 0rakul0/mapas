import pandas as pd

# Carregue os dados do arquivo CSV
mapa_poligono = pd.read_csv('data_master/table_contiguity_queen.csv', sep=',')

# Obtenha a lista de todas as UF (estados)
ufs = mapa_poligono['uf_mun1'].unique()

# Itere sobre cada UF e crie a matriz correspondente
for uf in ufs:
    # Filtrar os dados para a UF atual
    uf_df = mapa_poligono[(mapa_poligono['uf_mun1'] == uf) | (mapa_poligono['uf_mun2'] == uf)]

    # Crie uma lista de municípios únicos para a UF atual
    municipios = sorted(set(uf_df['ibge_mun1'].unique()) | set(uf_df['ibge_mun2'].unique()))

    # Crie uma matriz de zeros para a UF atual
    n = len(municipios)
    matrix = [[0] * n for _ in range(n)]

    # Preencha a matriz com 1 onde os municípios se tocam
    for _, row in uf_df.iterrows():
        municipio1 = row['ibge_mun1']
        municipio2 = row['ibge_mun2']
        i = municipios.index(municipio1)
        j = municipios.index(municipio2)
        matrix[i][j] = 1
        matrix[j][i] = 1
        # print(municipio1, municipio2)

    # Converta a matriz em um DataFrame com os nomes dos municípios como índice
    matrix_df = pd.DataFrame(matrix, columns=municipios, index=municipios)

    # Classifique o DataFrame alfabeticamente pelo nome dos municípios
    matrix_df = matrix_df.reindex(sorted(matrix_df.columns), axis=1)

    # Salve a matriz em um arquivo CSV com o nome da UF
    matrix_df.to_csv(f'output_ibge_externo/matriz_toque_{uf}_ibge.csv', index=True, header=True)

    # Exiba a matriz ou faça o que for necessário com ela
    print(f'Matriz para a UF {uf}:')
    print(matrix_df)
