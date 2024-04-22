# balíčky -----------------------------------------------------------------
library(tidyverse)
library(easystats)


# příprava dat pro ukázky -------------------------------------------------

# tvorba sloupce s faktorem, pro test
mtcars <- mtcars %>%
    mutate(am_fac = as_factor(am))

# tvorba t-testu
test <- t.test(mpg ~ am_fac, data = mtcars)

# tvorba jednoduchého linárního modelu
model <- lm(Sepal.Length ~ Species, data = iris)

# použití balíku report ---------------------------------------------------

# data
report(mtcars)

# výsledek testu
report(test)

# výsledek modelu
report(model)

# textové vyhodnocení p-value
report_s(p = 0.005)

# použití balíku insight --------------------------------------------------

iris_with_model <- iris %>%
    mutate(
        estimated = get_predicted(model),
        estimated_ci = get_predicted_ci(model)
    )

# použití balíku performance ----------------------------------------------

performance(model)

# použití balíku parameters -----------------------------------------------

model_parameters(model)

# použití balíku see ------------------------------------------------------

plot(check_model(model))

plot(parameters(model))
