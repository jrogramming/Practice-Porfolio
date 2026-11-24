# Libraries

library(dplyr)
library(stringr)


# Cleaning

rawdata <- read.csv("stylevana-raw.csv")

clean <- (rawdata[,c(4,5,6,8,11,16,17)])

colnames(clean)<- c("Product","OriginalPrice", "SalePrice", "Attributes", "Stars", "Description", "Brand")

# Removes row
RRdata <- clean[!grepl("#NAME?", clean$Description), ]

# Removes cell
RCdata <- clean %>% mutate(clean$Description, "#NAME?")

#View(data)

