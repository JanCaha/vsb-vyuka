import rasterio
from utils import data_path

if __name__ == "__main__":

    ds: rasterio.DatasetReader

    no_data_value = 0

    with rasterio.open(data_path("HYP_HR_SR_W.tif")) as input_ds:

        band_number = 1
        band_values = input_ds.read(band_number)
        data_type = input_ds.dtypes[band_number]

        with rasterio.open(
            data_path("single_band_raster.tif"),
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

            row = int(input_ds.height / 2)
            for i in range(input_ds.width):
                band_values[row, i] = 255
                band_values[int(input_ds.height / 4), i] = no_data_value

            output_ds.write(band_values, 1)
