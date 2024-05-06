# knihovny ----------------------------------------------------------------

library(tidyverse)
library(performance) # easystats
library(parameters) # easystats

# příprava data -----------------------------------------------------------

data(iris)

iris_selected <- iris %>% 
  select(1:4)

# kontrola vhodnosti ------------------------------------------------------

performance::check_clusterstructure(iris_selected)

# výběr počtu shluků ------------------------------------------------------

n <- n_clusters(iris_selected, package = c("easystats", "NbClust", "mclust"))

plot(n)


# k means elbow method ----------------------------------------------------

x <- n_clusters_elbow(iris_selected)
x
as.data.frame(x)
plot(x)

# shlukování k-means ------------------------------------------------------

kmeans_clusters <- cluster_analysis(iris_selected, n = 3, method = "kmeans")

kmeans_clusters
  
plot(summary(kmeans_clusters))

plot(kmeans_clusters)

iris_selected <- iris %>% 
  mutate(predicted_cluster_kmeans = predict(kmeans_clusters))


# shlukování hclust -------------------------------------------------------

hclust_clusters <- cluster_analysis(iris_selected, n = 3, method = "hclust")

plot(summary(kmeans_clusters))

plot(kmeans_clusters)

iris_selected <- iris %>% 
  mutate(predicted_cluster_hclust = predict(kmeans_clusters))

