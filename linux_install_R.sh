ALL_PACKAGES=false
GGPLOT2=false
while getopts "ag" opt; do
  case $opt in
    a)
      ALL_PACKAGES=true
      ;;
    g)
      GGPLOT2==true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Prepare and install R
sudo wget -q https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc -O /etc/apt/trusted.gpg.d/marutter_pubkey.asc
echo "deb [signed-by=/etc/apt/trusted.gpg.d/marutter_pubkey.asc] https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/" | sudo tee /etc/apt/sources.list.d/r.list
sudo apt-get update
sudo apt-get install -y r-base

# Prepare and install R packages from binaries (otherwise it takes forever to compile them from source)    
sudo wget -q https://eddelbuettel.github.io/r2u/assets/dirk_eddelbuettel_key.asc -O /etc/apt/trusted.gpg.d/cranapt_key.asc
echo "deb [arch=amd64] https://r2u.stat.illinois.edu/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/cranapt.list
sudo apt-get update

if [ "$ALL_PACKAGES" = true ]; then
    sudo apt-get install -y \
        r-cran-sf r-cran-terra r-cran-raster r-cran-stars r-cran-tmap \
        r-cran-tidyverse r-cran-tidymodels \
        r-cran-here \
        r-cran-dt \
        r-cran-rmarkdown \
        r-cran-plotly \
        r-cran-easystats
fi

if [ "$GGPLOT2" = true ]; then
    sudo apt-get install -y r-cran-ggplot2
fi