# result.csv(made by identify.py) is required. output cluster result into cluster.pdf

library(readr)
library(pacman) #install.packages("pacman")
library(RColorBrewer)
library(amap)
library(dendextend)
pacman::p_load(amap, dplyr, RColorBrewer, dendextend)

data <- read_csv("data/result.csv", col_names = FALSE)
# feature selection
feature_idx = c(1,10:12,21:23)
data <- data[feature_idx]
rownames(data) <- data$X1
data$X1 <- NULL

d <- dist(data, method="euclidean")
print(d)
clst <- hclust(d, method="ward.D")

den <- as.dendrogram(clst)
n <- ceiling(nrow(data) / 2) 
col3 <- brewer.pal(9, "Set1")
col.cl3 <- col3[cutree(clst, k=n, order_clusters_as_data = F)]
den <- den %>%
    dendextend::set("labels_colors", value = col.cl3) %>%
    dendextend::set("branches_k_color", k=n, col3)

pdf("cluster.pdf")
plot(den)
dev.off()
