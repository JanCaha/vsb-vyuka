#!/bin/bash

ALL_PACKAGES=false
GGPLOT2=false

function usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "    -a,--all           Install all R packages."
    echo "    -g,--ggplot2       Install ggplot2 package."
    echo "    -h,--help          Display the usage and exit."
}

OPTS=`getopt --options agh \
         --long all,ggplot2,help \
         --name "$0" -- "$@"`
eval set -- "$OPTS"

while true; do
  case $1 in
    -a|--all)
      ALL_PACKAGES=true
      shift
      ;;
    -g|--ggplot2)
      GGPLOT2=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
	if [ ! -z $2 ];
      then
        echo "Invalid parameter: $2"
        exit 1
      fi
      break
      ;;
    *)
      echo "Invalid option"
      exit 1
      ;;
  esac
done

echo "Install all packages - $ALL_PACKAGES"
echo "Install ggplot2 package - $GGPLOT2"

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
  echo "Installing all R packages"
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
  echo "Installing ggplot2 package"
  sudo apt-get install -y r-cran-ggplot2
fi