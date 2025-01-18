from osgeo import gdal
from utils import data_path, save_data_path

gdal.UseExceptions()

if __name__ == "__main__":
    file = data_path("HYP_HR_SR_W.tif")
    result_file_clipped = save_data_path("clipped.jpg")

    options = gdal.TranslateOptions(format="JPEG", projWin=[11, 52, 18.5, 47])

    gdal.Translate(result_file_clipped, file, options=options)

    result_file_warped = save_data_path("warped.tif")
    options = gdal.WarpOptions(
        format="GTiff",
        dstSRS="EPSG:5514",
        resampleAlg="bilinear",
        xRes=200,
        yRes=200,
    )

    gdal.Warp(result_file_warped, result_file_clipped, options=options)
