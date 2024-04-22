# instalace balíčků -------------------------------------------------------

install.packages(c("remotes", "qgisprocess"))
remotes::install_github("JanCaha/r_package_qgis")


# načtení prostorových dat ------------------------------------------------

library(sf)
nc <- st_read(system.file("shape/nc.shp", package = "sf"), quiet = TRUE)


# výpočet bufferu pomocí QGIS a načtení dat zpět do R ---------------------

buffered <- qgis::qgis_buffer(
    INPUT = nc,
    DISTANCE = 0.5,
    END_CAP_STYLE = "Flat",
    .quiet = TRUE
) %>%
    st_as_sf()
