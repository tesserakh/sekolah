# Path customization
#setwd("~/jobs/freelance/Upwork/2 Progress/Data Sekolah for Isaac/sekolah")
path <- "data/main"

# Import and combine data
sekolah <- list.files(path, "data[0-9].*csv", full.names = TRUE)
sekolah <- lapply(sekolah, read.csv)
sekolah <- do.call(rbind, sekolah)

# Cleanup subdistrict
sekolah$Subdistrict <- gsub("[-,\\.]\\s?", "", sekolah$Subdistrict)
sekolah$Name <- stringr::str_squish(sekolah$Name)

# Sorting data
sekolah <- with(sekolah, sekolah[order(Level, Status, Province, City),])

# Save to csv
write.csv(sekolah, "data/data.csv", row.names = FALSE)


# Function
separate_profile_urls <- function(data, path_store, div) {
  if (missing(div)) divided_by <- 2000
  n_len <- floor(nrow(data) / divided_by)
  n_end <- nrow(data) %% divided_by
  group <- c(rep(1:n_len, each = divided_by), rep(n_len + 1, n_end))
  linklist <- split(data["Link"], group)
  
  for (x in 1:length(linklist)) {
    namefile <- sprintf(paste0(path_store, "/url%s.txt"), x)
    print(sprintf("Saving to %s", namefile))
    write.table(x = linklist[[x]],
                file = namefile,
                quote = FALSE,
                sep = "\n",
                col.names = FALSE,
                row.names = FALSE)
  }
}


# Create url list by SMA level
nrow(sekolah[sekolah$Level == "SMA",])
sma <- sekolah[sekolah$Level == "SMA",]
if (!dir.exists("data/url/sma")) dir.create("data/url/sma")
separate_profile_urls(sma, "data/url/sma", 2000)


# Create url list into n-separated txt files
nrow(sekolah[sekolah$Level != "SMA",])
nonsma <- sekolah[sekolah$Level != "SMA",]
if (!dir.exists("data/url/nonsma")) dir.create("data/url/nonsma")
separate_profile_urls(sekolah, "data/url/nonsma", 2000)

