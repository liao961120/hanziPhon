library(readr)
library(magrittr)
library(jsonlite)

col <- readLines("selected.tsv") %>% strsplit("\t")

d <- read_csv("廣韻(20170209).csv",
              col_types = cols(.default = col_character()))
d <- d[, sapply(col, function(x) x[1])]
colnames(d) <-  sapply(col, function(x) x[2])

# s = "fan_qie pinyin ipa"
s = "反切 拼音 IPA"
for (c in strsplit(s, " ")[[1]] )
    d[[c]] <- strsplit(d[[c]], "/")

writeLines(jsonlite::toJSON(d, pretty=F), "GuangYun.json")
