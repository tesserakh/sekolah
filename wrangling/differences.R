# Difference number between scraped data and data need to be scraped

setwd("~/jobs/freelance/Upwork/2 Progress/Data Sekolah for Isaac/sekolah")

levels <- read.csv("levels.csv")
scrape_data <- nrow(read.csv("data/data.csv"))
needed_data <- sum(levels$negeri) + sum(levels$swasta)
needed_data - scrape_data
