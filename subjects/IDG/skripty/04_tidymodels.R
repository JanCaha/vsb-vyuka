# balíčky -----------------------------------------------------------------

library(tidyverse)
library(tidymodels)

# data --------------------------------------------------------------------

iris_split <- initial_split(iris, prop = 0.6)

# recipe ------------------------------------------------------------------

iris_recipe <- training(iris_split) %>%
    recipe(Species ~ .) %>%
    step_corr(all_predictors()) %>%
    step_center(all_predictors(), -all_outcomes()) %>%
    step_scale(all_predictors(), -all_outcomes()) %>%
    prep()

iris_recipe

iris_testing <- iris_recipe %>%
    bake(testing(iris_split))

iris_training <- iris_recipe %>%
    bake(new_data = NULL)

glimpse(iris_testing)

# model -------------------------------------------------------------------

base_model <- rand_forest(trees = 100, mode = "classification")

iris_ranger <- base_model %>%
    set_engine("ranger")

iris_rf <- base_model %>%
    set_engine("randomForest")

iris_rf %>%
    translate()

# fit ---------------------------------------------------------------------

iris_ranger_fit <- iris_ranger %>%
    fit(Species ~ ., iris_training)

iris_rf_fit <- iris_rf %>%
    fit(Species ~ ., iris_training)

# predict -----------------------------------------------------------------

iris_ranger_pred <- iris_ranger_fit %>%
    predict(iris_testing) %>%
    bind_cols(iris_testing)

iris_rf_pred <- iris_rf_fit %>%
    predict(iris_testing) %>%
    bind_cols(iris_testing)

iris_ranger_pred <- iris_ranger_fit %>%
    predict(iris_testing, type = "prob") %>%
    bind_cols(iris_ranger_pred)

iris_rf_pred <- iris_rf_fit %>%
    predict(iris_testing, type = "prob") %>%
    bind_cols(iris_rf_pred)

# evaluate ----------------------------------------------------------------

iris_ranger_pred %>%
    metrics(truth = Species, estimate = .pred_class)

iris_rf_pred %>%
    metrics(truth = Species, estimate = .pred_class)

iris_ranger_pred %>%
    gain_curve(Species, .pred_setosa:.pred_virginica) %>%
    autoplot()

iris_rf_pred %>%
    gain_curve(Species, .pred_setosa:.pred_virginica) %>%
    autoplot()

iris_ranger_pred %>%
    metrics(Species, .pred_setosa:.pred_virginica, estimate = .pred_class)

iris_rf_pred %>%
    metrics(Species, .pred_setosa:.pred_virginica, estimate = .pred_class)
