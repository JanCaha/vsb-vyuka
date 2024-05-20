# knihovny ----------------------------------------------------------------
install.packages(c(psych))

library(tidyverse)
library(performance) # easystats
library(parameters) # easystats
library(psych)

# příprava data -----------------------------------------------------------

data(iris)

iris_selected <- iris %>% 
  select(1:4)

# kontrola vhodnosti ------------------------------------------------------

performance::check_factorstructure(iris_selected)

# počet faktorů -----------------------------------------------------------

factors_n <- n_factors(iris_selected, type = "FA")

factors_n

as.data.frame(factors_n)

# faktorová analýza -------------------------------------------------------

iris_fa <- psych::fa(iris_selected, nfactors = 2) %>%
  model_parameters(sort = TRUE, threshold = "max")

iris_fa
