# knihovny ----------------------------------------------------------------

library(tidyverse)
library(see) # easystats
library(parameters) # easystats
library(performance) # easystats

# příprava data -----------------------------------------------------------

data(iris)

iris_selected <- iris %>% 
  select(1:4)

# PCA ---------------------------------------------------------------------

pca <- principal_components(iris_selected, n = 2)

pca


# výpočet PCA -------------------------------------------------------------

pca_scores <- predict(pca, names = c("PCA_1", "PCA_2"))

pca_scores <- pca_scores %>% 
  mutate(cluster =  iris$Species)

# vizualizace ------------------------------------------------------------

ggplot(pca_scores, aes(x = PCA_1, y = PCA_2, color = cluster)) +
  geom_point()  + 
  theme_bw()
