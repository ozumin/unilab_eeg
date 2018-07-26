# result.csv(made by identify.py) is required. output cluster result into cluster.pdf

library(readr)
data <- read_csv("data/result.csv", col_names = FALSE)
# feature selection
feature_idx = c(1,10:12,21:23)
data <- data[feature_idx]
rownames(data) <- data$X1
data$X1 <- NULL

d <- dist(data, method="euclidean")
print(d)
clst <- hclust(d, method="ward.D")
pdf("cluster.pdf")
plot(clst)
dev.off()
