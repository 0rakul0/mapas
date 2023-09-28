import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

class mapa():
    def create_grid(self, gdf, batch_size=100):
        vizinhanca = []
        num_batches = len(gdf) // batch_size
        for batch_idx in range(num_batches + 1):
            batch_start = batch_idx * batch_size
            batch_end = (batch_idx + 1) * batch_size
            batch = gdf.iloc[batch_start:batch_end]

            # Itere sobre cada par de municípios para identificar seus vizinhos
            for index, municipio_a in batch.iterrows():
                for _, municipio_b in gdf.iterrows():
                    if municipio_a['NM_MUN'] != municipio_b['NM_MUN'] and municipio_a['geometry'].touches(
                            municipio_b['geometry']):
                        vizinhanca.append({
                            "ibge_mun1": municipio_a['CD_MUN'],
                            "ibge_mun2": municipio_b['CD_MUN'],
                            "uf_mun1": municipio_a['SIGLA_UF'],
                            "uf_mun2": municipio_b['SIGLA_UF'],
                            "municipio_1": municipio_a['NM_MUN'],
                            "municipio_2": municipio_b['NM_MUN']
                        })
        return vizinhanca


if __name__ == "__main__":
    m = mapa()
    shapefile_path = "BR_municipios_2022.shp"
    gdf = gpd.read_file(shapefile_path, encoding='utf-8')

    print('tamanho', gdf.shape)

    # Use o joblib para paralelizar o processamento em lotes
    num_jobs = 8  # Ajuste o número de jobs conforme necessário
    batch_size = 100  # Ajuste o tamanho do lote conforme necessário
    batches = [gdf.iloc[i:i + batch_size] for i in range(0, len(gdf), batch_size)]

    with Parallel(n_jobs=num_jobs) as parallel:
        grupos = parallel(delayed(m.create_grid)(batch) for batch in batches)

    # Concatene os resultados dos lotes em uma única lista
    grupo = [item for sublist in grupos for item in sublist]

    # Crie um DataFrame a partir da lista de vizinhanças
    df_vizinhanca = pd.DataFrame(grupo)

    # Salve o DataFrame em um arquivo CSV
    df_vizinhanca.to_csv('vizinhos_municipios.csv', index=False, quoting=1)