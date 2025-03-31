import rasterio
from utils import data_path, save_data_path

if __name__ == "__main__":

    input_ds: rasterio.DatasetReader

    no_data_value = 0

    # context manager rasteru pr čtení
    with rasterio.open(data_path("HYP_HR_SR_W.tif")) as input_ds:

        print(f"Number of bands: {input_ds.count}.")
        print(f"Size: {input_ds.width} - {input_ds.height}.")

        band_types = {i: dtype for i, dtype in zip(input_ds.indexes, input_ds.dtypes)}
        band_types_str = "\n\t".join([f"{key}: {value}" for key, value in band_types.items()])

        print(f"Band types: \n\t{band_types_str}")

        print(f"Crs: {input_ds.crs}")
        print(f"Bounds: {input_ds.bounds}")
        print(f"Transform: \n{input_ds.transform}")

        print("-" * 10)

        # informace o rasteru a výpis
        band_number = 1
        band_values = input_ds.read(band_number)
        data_type = input_ds.dtypes[band_number]

        # context manager rasteru pro zápis
        with rasterio.open(
            save_data_path("single_band_raster.tif"),
            "w",
            driver="GTiff",
            height=input_ds.height,
            width=input_ds.width,
            count=1,
            dtype=data_type,
            crs=input_ds.crs,
            transform=input_ds.transform,
            nodata=no_data_value,
        ) as output_ds:

            # modifikace hodnot
            row = int(input_ds.height / 2)
            for i in range(input_ds.width):
                band_values[row, i] = 255
                band_values[int(input_ds.height / 4), i] = no_data_value

            # zápis pásma do rastru
            output_ds.write(band_values, 1)
