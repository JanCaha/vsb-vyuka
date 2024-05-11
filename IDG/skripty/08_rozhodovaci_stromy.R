# knihovny ----------------------------------------------------------------

library(tidyverse)
library(tidymodels)
library(rpart.plot)

# příprava data -----------------------------------------------------------

data(iris)

# recept ------------------------------------------------------------------

rec <- recipe(Species ~ ., iris)

# vytvoření modelu ------------------------------------------------

decision_tree(mode = "classification", tree_depth = 5)

dec_tree <- decision_tree() %>%
  set_mode("classification") %>%
  set_engine("rpart")


# fit modelu --------------------------------------------------------------

dec_tree_fit <- dec_tree %>%
  fit(Species ~ ., data = iris)

dec_tree_fit

dec_tree_fit %>%
  extract_fit_engine() %>%
  rpart.plot()


# hodnocení modelu --------------------------------------------------------

pred_iris <- augment(dec_tree_fit, new_data = iris) 

pred_iris %>%
  accuracy(truth = Species, estimate = .pred_class)

pred_iris %>%
  conf_mat(truth = Species, estimate = .pred_class)
