needed_packages <- c(
    "tidyverse",
    "here",
    "sf",
    "terra",
    "stars",
    "tmap",
    "lwgeom",
    "qgisprocess",
    "remotes",
    "tidymodels",
    "DT",
    "rmarkdown",
    "plotly",
    "tidymodels",
    "easystats"
)

# nejjednodušší způsob instalace balíčků by bylo prosté volání install.packages(needed_packages),
# ale to by znamenalo, že by se balíčky instalovaly i když už jsou nainstalované, což je zbytečné a zdlouhavé
# následující kód tedy instaluje jen ty balíčky, které ještě nejsou nainstalované, ale kód je komplikovanější

new_packages <- needed_packages[!(needed_packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages)

remotes::install_github("JanCaha/r_package_qgis")
