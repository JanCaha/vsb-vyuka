import rasterio
from utils import data_path

if __name__ == "__main__":

    ds: rasterio.DatasetReader

    with rasterio.open(data_path("HYP_HR_SR_W.tif")) as ds:
        print(f"Number of bands: {ds.count}.")
        print(f"Size: {ds.width} - {ds.height}.")

        band_types = {i: dtype for i, dtype in zip(ds.indexes, ds.dtypes)}
        band_types_str = "\n\t".join([f"{key}: {value}" for key, value in band_types.items()])

        print(f"Band types: \n\t{band_types_str}")

        print(f"Crs: {ds.crs}")
        print(f"Bounds: {ds.bounds}")
        print(f"Transform: \n{ds.transform}")

        print("-" * 10)

        band_array = ds.read(1)

        print(band_array)
