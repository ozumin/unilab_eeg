data <- read.csv("result.csv", row.names=1)

#data <- data[c(2,4,7,15,21),]

d <- dist(data[,c(1,3,5,6,7,10,18)], upper=TRUE, diag=TRUE, method="manhattan")

clst <- hclust(d, method="ward.D")

pdf("cluster.pdf")
plot(clst)
dev.off()
