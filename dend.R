library(StatMatch)
library(proxy)

data <- read.csv("result.csv", row.names=1)
#data <- data[c(2,4,7,15,21),]

n = 7 # number of people

sam <- sample(1:n, 4)

rand <- c()
for(i in sam){
    rand <- append(rand, sample(((i-1)*5+1):(i*5), 2))
}

#variable <- c(1,3,5,6,7,10,18)
#variable <- c(1,3,5,6,7,10)
#variable <- c(1:8)
variable <- c(9:11)
#variable <- c(1:11)
#variable <- c(1:22)

dat <- data[rand, variable]
#d <- mahalanobis.dist(dat)
d <- proxy::dist(dat, method="mahalanobis")
print(d)
clst <- hclust(d, method="ward.D")

pdf("cluster.pdf")
plot(clst)
dev.off()
