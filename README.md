# Origem dos dados

Usei duas fontes de dados para montar o mapa de vizinha, um foi cedido pelo IPEA e o outro pelo IBGE, o link dos arquivos *.shp estão no link abixo
[LINK_DOS_MUNICIPIOS_IBGE](https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_Municipios_2022.zip)
[LINK_CONTORNO_DO_PAIS_IBGE](https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_Pais_2022.zip)
o arquivo que gera esses vizinhos municipais é [mapas_ibge_shp.py](https://github.com/0rakul0/mapas/blob/87a60c0c4fe31ab34ab282f5fd3e1fbd0238a538/mapas_ibge_shp.py)

# Projeto de Análise de Mapas e Matrizes

Este é um projeto de análise de mapas que inclui a criação de matrizes de adjacência para representar a contiguidade de municípios em diferentes UF.

Autor: Jefferson Silva dos Anjos
Licença: MIT License

## Criação de Matrizes de Adjacência

Aqui está o código que cria as matrizes de adjacência com base nos dados do arquivo CSV:

```python
import pandas as pd

mapa_poligono = pd.read_csv('data_master/table_contiguity_queen.csv', sep=',')

# lista de todas as UF (estados)
ufs = mapa_poligono['uf_mun1'].unique()

for uf in ufs:
    # Filtrar os dados para a UF atual
    uf_df = mapa_poligono[(mapa_poligono['uf_mun1'] == uf) | (mapa_poligono['uf_mun2'] == uf)]

    # lista de municípios únicos para a UF atual
    municipios = sorted(set(uf_df['ibge_mun1'].unique()) | set(uf_df['ibge_mun2'].unique()))

    # matriz de zeros para a UF atual
    n = len(municipios)
    matrix = [[0] * n for _ in range(n)]

    # Aqui a matriz é preenchida com 1 onde os municípios se tocam
    for _, row in uf_df.iterrows():
        municipio1 = row['ibge_mun1']
        municipio2 = row['ibge_mun2']
        i = municipios.index(municipio1)
        j = municipios.index(municipio2)
        matrix[i][j] = 1
        matrix[j][i] = 1
        # print(municipio1, municipio2)

    # DataFrame com os nomes dos municípios como índice
    matrix_df = pd.DataFrame(matrix, columns=municipios, index=municipios)

    # ordenação do dos municípios
    matrix_df = matrix_df.reindex(sorted(matrix_df.columns), axis=1)

    # Salva a matriz em um arquivo CSV com o nome da UF
    matrix_df.to_csv(f'output_ibge_externo/matriz_toque_{uf}_ibge.csv', index=True, header=True)

    # exibe a matriz
    print(f'Matriz para a UF {uf}:')
    print(matrix_df)
```

### Criação de Matrizes de Adjacência

Nesta seção, o código carrega dados de um arquivo CSV contendo informações sobre a contiguidade de municípios em diferentes UF (estados). Ele itera sobre cada UF, cria matrizes de adjacência representando a contiguidade e salva essas matrizes em arquivos CSV separados.

#### Passos

1. Carregar dados do arquivo CSV.
2. Iterar sobre cada UF (estado).
3. Filtrar dados para a UF atual.
4. Criar uma lista de municípios únicos.
5. Criar uma matriz de zeros e preenchê-la com 1s onde os municípios se tocam.
6. Salvar a matriz em um arquivo CSV com o nome da UF.
7. Exibir a matriz ou realizar outras operações necessárias.
