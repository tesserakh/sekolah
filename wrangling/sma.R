library(dplyr, warn.conflicts = FALSE)
library(stringr)

# Path customization
#setwd("~/jobs/freelance/Upwork/2 Progress/Data Sekolah for Isaac/sekolah")
path <- "data/profile"

# Import and combine data
sekolah <- list.files(path, "profile_sma[0-9].*csv", full.names = TRUE)
sekolah <- lapply(sekolah, read.csv)
sekolah <- do.call(rbind, sekolah)

# Select needed columns 
sekolah_detail <- sekolah %>% 
  select(Link, 
         Address, 
         Akreditasi, 
         Kepala.Sekolah, 
         Guru, 
         Siswa.Laki.laki,
         Siswa.Perempuan,
         Rombongan.Belajar,
         Kurikulum,
         Semester.Data,
         Ruang.Kelas) %>% 
  as_tibble() %>% 
  distinct()

# Check unscraped link
# path <- "data/url/sma"
# url <- list.files(path, "txt", full.names = TRUE) |> 
#   lapply(function(file) {read.table(file, header = FALSE, sep = "\n")[[1]]})
# url <- do.call(c, url)

# Create additional link that failed being scraped
# x <- c()
# for (u in seq_along(url)) {
#   if (url[u] %in% sekolah[["Link"]]) {
#     x <- append(x, TRUE)
#   } else {
#     x <- append(x, FALSE)
#   }
# }
# 
# url[!x]

sekolah_v1 <- readr::read_csv("data/sekolah-v1.csv")

sekolah_v2 <- left_join(sekolah_detail, sekolah_v1, by = "Link") %>% distinct()
sekolah_v2 %>% View()
names(sekolah_v2)
sekolah_v2 <- sekolah_v2 %>% 
  arrange(Province, City, Subdistrict, Level, Status) %>% 
  mutate(Ruang.Kelas = as.integer(str_remove(Ruang.Kelas, '\\*')),
         Siswa.Laki.laki = as.integer(Siswa.Laki.laki),
         Siswa.Perempuan = as.integer(Siswa.Perempuan)) %>% 
  select(NPSN,
         Name,
         Level,
         Status,
         Address,
         Subdistrict,
         City,
         Province,
         Akreditasi, 
         Kepala.Sekolah, 
         Guru, 
         Siswa.Laki.laki,
         Siswa.Perempuan,
         Rombongan.Belajar,
         Kurikulum,
         Semester.Data,
         Ruang.Kelas,
         Link)
headers <- names(sekolah_v2)
headers <- str_replace_all(headers, "\\.", " ")
names(sekolah_v2) <- headers
readr::write_csv(sekolah_v2, file = "data/sekolah-v2-level-sma.csv", na = "")
