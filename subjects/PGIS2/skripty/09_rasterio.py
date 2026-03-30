# NOTE: Ukázka čtení rastru pomocí Rasterio, výpis metadat a zápis jednoho upraveného pásma do nového souboru
import rasterio
from utils import data_path, save_data_path

if __name__ == "__main__":

    # obdobně jako u GDAL je vhodné deklarovat typ proměnné, protože rasterio nevrací konkrétní typ
    input_ds: rasterio.DatasetReader

    no_data_value = 0

    # context manager rasteru pro čtení
    with rasterio.open(data_path("HYP_HR_SR_W.tif")) as input_ds:

        print(f"Počet pásem: {input_ds.count}.")
        print(f"Rozměry: {input_ds.width} - {input_ds.height}.")

        band_types = {i: dtype for i, dtype in zip(input_ds.indexes, input_ds.dtypes)}
        band_types_str = "\n\t".join([f"{key}: {value}" for key, value in band_types.items()])

        print(f"Datové typy pásem: \n\t{band_types_str}")

        print(f"Souřadnicový systém: {input_ds.crs}")
        print(f"Rozsah: {input_ds.bounds}")
        print(f"Transformace: \n{input_ds.transform}")

        print("-" * 10)

        # informace o rastru a načtení do paměti jako pole (ndarray)
        band_number = 1
        band_values = input_ds.read(band_number)

        # vytvoření rastrového profilu (metadat) pro nový soubor zkopírováním z původního
        profile = input_ds.profile
        profile.update(count=1, driver="GTiff", nodata=no_data_value)  # omezíme se jen na jedno pásmo

        # context manager rastru pro zápis s využitím rozbalení profilu kwargs operátorem **
        with rasterio.open(save_data_path("single_band_raster.tif", delete_if_exist=True), "w", **profile) as output_ds:

            # určení indexů řádků
            max_value_row = input_ds.height // 2
            no_data_row = input_ds.height // 4

            # modifikace hodnot celoplošně pomocí vektorizace NumPy (bez pomalých for cyklů)
            band_values[max_value_row, :] = 255
            band_values[no_data_row, :] = no_data_value

            # zápis upraveného pole jako prvního pásma
            output_ds.write(band_values, 1)
