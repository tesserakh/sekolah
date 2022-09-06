library(dplyr, warn.conflicts = FALSE)
library(purrr)
library(readr)
library(stringr)

# Path customization
# Make sure the working directory is sekolah
# getwd()
path <- "data/profile"

# Import and combine data
# sekolah <- list.files(path, "profile[0-9].*csv", full.names = TRUE)
sekolah <- list.files(path, "*csv", full.names = TRUE)
sekolah <- map_df(
  sekolah, 
  ~read_csv(
    file = .x,
    col_types = cols(
      Guru = col_integer(), 
      `Siswa Laki-laki` = col_integer(), 
      `Siswa Perempuan` = col_integer(), 
      `Rombongan Belajar` = col_integer(), 
      Kurikulum = col_character()
    )
  )
)

# Select needed columns 
sekolah_filter <- sekolah %>% 
  select(Link, 
         Address, 
         Akreditasi, 
         `Kepala Sekolah`, 
         Guru, 
         `Siswa Laki-laki`,
         `Siswa Perempuan`,
         `Rombongan Belajar`,
         Kurikulum,
         `Semester Data`,
         `Ruang Kelas`) %>% 
  distinct()

# Check duplicated data
find_duplication_link <- function(data, colname) {
  dup <- duplicated(data[[colname]])
  link <- data[dup,][[colname]]
  return(link)
}

dup_link <- find_duplication_link(sekolah_filter, "Link")

sekolah_filter %>% 
  filter(Link %in% dup_link) %>% 
  arrange(Address) %>% 
  View()

# Check unscraped link
path <- "data/urls/"
urls <- list.files(path, "txt", full.names = TRUE)
urls <- map_df(urls, ~read.table(.x, header = FALSE, sep = "\n"))
urls <- urls$V1
urls <- unique(urls)

length(sekolah_filter$Link)
length(urls)

sekolah_filter <- filter(sekolah_filter, Link %in% urls)
nrow(sekolah_filter)

# Join data
sekolah_v1 <- read_csv("data/sekolah-v1.csv") %>% distinct()
sekolah_v2 <- full_join(
  sekolah_filter, 
  sekolah_v1, 
  by = "Link") %>% 
  distinct()

sekolah_v2 <- sekolah_v2 %>% 
  arrange(Level, Status, Province, City, Subdistrict, Address) %>% 
  mutate(`Ruang Kelas` = str_remove(`Ruang Kelas`, '\\*')) %>% 
  select(NPSN,
         Name,
         Level,
         Status,
         Address,
         Subdistrict,
         City,
         Province,
         Akreditasi, 
         `Kepala Sekolah`, 
         Guru, 
         `Siswa Laki-laki`,
         `Siswa Perempuan`,
         `Rombongan Belajar`,
         Kurikulum,
         `Semester Data`,
         `Ruang Kelas`,
         Link)
write_csv(sekolah_v2, file = "data/sekolah-v2.csv", na = "")

# Summary
# 555,898 of 556,034 data