library(dplyr)
library(lubridate)
library(ggplot2)
library(arules)
library(lattice)
library(clValid)
library(multisom)
library(SOMbrero)
library(NbClust)
library(clusterCrit)
library(fpc)
library(factoextra)


c <-read.csv("dataset.csv",header = T,encoding="UTF-8") 
c2 <- c[,2:3]#Select only reactions values

#normalization of dataset variables

norm=(c2-min(c2))/(max(c2)-min(c2))

#The function returns internal indexes to clustering validation

intern <- clValid(norm, 2:3, clMethods=c("fanny"), validation="internal", maxitems=4700, metric="euclidean", memb.exp=1.5)
summary(intern)

#Fanny algorithm
x=c(1.5, 1.8) #Valores de índices de fuzzificação

for(i in x){
  
  print(i)
  fan <- fanny(norm, 3, diss=F, memb.exp = i, metric = "euclidean", maxit = 500)
  fan$silinfo
}

#Nbclust k-means
results <- NbClust(data=norm, distance="euclidean", min.nc=2, max.nc=10, method="kmeans", index="dunn")

#K-means with new parameters

x=c(10, 20, 25)

for(i in x){
  
  print(i)
  km <- kmeans(norm, 4, iter.max=100, nstart = 10)
  
  diss <- daisy(norm)
  
  sk <- silhouette(km$cluster, diss)
  
  #Plot para os valores dos índices de silhouette
  fviz_silhouette(sk)
  
}

#To identify components inside clusters
c2$cluster <- km$cluster

for (i in 1:4){
  
  #Assign cluster 1 to data_clus1, cluster 2 to data_clus2, and so on...
  assign(paste0("data_clus",i), c2[c2$cluster==i,])
  #data_clus1(to print cluster 1)
}


#Multisom algorithm returns the optimal number of clusters for each SOM layer 

res <- multisom.batch(norm, xheight = 7, xwidth = 7, "hexagonal", min.radius=0.00010, 
                      max.radius=0.002, maxit = 1000, radius.type = "gaussian", alpha=1, init="random", "dunn")

res

