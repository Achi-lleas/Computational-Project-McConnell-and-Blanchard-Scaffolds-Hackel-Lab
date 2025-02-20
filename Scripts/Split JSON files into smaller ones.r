# Achilleas Thomas (Achi-lleas) 02/19/2025
# This is a script that splits a large JSON file into smaller ones (100 entries each).
# We need this script because AlphaFold3 only accepts JSON files with 100 or fewer jobs.

library(rjson)
library(glue)

scaffolds <- list("Blanchard", "McConnell") # The names, the file paths and other parameters can change for different applications of this script.

for (name in scaffolds) {
    all_jobs <- fromJSON(file = glue("./All sequences {name} JSON.json"))

    for (i in 0:((length(all_jobs) %/% 100) - 1)) {
        data <- c(all_jobs)[(1 + i * 100):(i * 100 + 100)]
        jsondata <- toJSON(data)
        write(jsondata, glue("./JSON split files/{name} {i+1}.json"))
    }

    data <- c(all_jobs)[(1 + (length(all_jobs) %/% 100) * 100):length(all_jobs)]
    jsondata <- toJSON(data)
    write(jsondata, glue("./JSON split/{name} {length(all_jobs) %/% 100 + 1}.json"))
}
