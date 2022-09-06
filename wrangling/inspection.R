library(dplyr, warn.conflicts = FALSE)
library(tidyr)

setwd("~/jobs/freelance/Upwork/2 Progress/Data Sekolah for Isaac/sekolah")

# Import data
levels <- readr::read_csv("levels.csv")
payload <- read.table("payload.txt")

# Inspect endpoint
payload$page <- gsub("^page=(\\d+).+$", "\\1", payload[[1]])

payload$school <- gsub(
  pattern = "\\+", replacement = " ",
  x = gsub("^.+pendidikan=(.+)\\&status.+$", "\\1", payload[[1]]))

payload$status <- gsub("^.+status_sekolah=(.+)$", "\\1", payload[[1]])

payload <- payload %>% 
  mutate(page = as.integer(page),
         status = tolower(status)) %>% 
  group_by(school, status) %>% 
  summarise(max_page = max(page), .groups = "drop")

levels <- levels %>% 
  arrange(school) %>% 
  pivot_longer(2:3, names_to = "status", values_to = "n") %>% 
  filter(n != 0) %>% 
  mutate(npage_must = ceiling(n/4))

left_join(
  levels %>% mutate(id = paste(school, status)),
  payload %>% mutate(id = paste(school, status), .keep = "unused"),
  by = "id") %>% 
  select(-id) %>% 
  mutate(max_page = ifelse(is.na(max_page), 0, max_page),
         needmore_page = npage_must - max_page) %>% 
  View()


# Inspect new payload.txt
payload_new <- read.table("payload_new.txt")
payload_old <- read.table("payload.txt")

waldo::compare(payload_old[[1]], payload_new[[1]])

sprintf("The differences: %s", nrow(payload_new) - nrow(payload_old))

payload_add <- payload_new %>% 
  mutate(appearance = ifelse(V1 %in% payload_old[[1]], TRUE, FALSE)) %>% 
  filter(appearance == FALSE) %>% 
  .[[1]]

write.table(x = payload_add, 
            file = "payload_add.txt", 
            quote = FALSE, 
            sep = "\n", 
            col.names = FALSE,
            row.names = FALSE)
