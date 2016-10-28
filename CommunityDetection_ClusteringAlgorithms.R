'''
This code apply K-means, Fanny and MultiSOM algorithms in datasets from OSN 
to detect communities of users that represents different engagement level around posts.

For more details about parameters, consult packages documentation:

https://cran.r-project.org/web/packages/clValid/clValid.pdf
https://cran.r-project.org/web/packages/NbClust/NbClust.pdf
https://cran.r-project.org/web/packages/multisom/multisom.pdf

@author: Ingrid Nascimento

'''
library(dplyr)
library(lubridate)
library(arules)
library(lattice)
library(clValid)
library(multisom)
library(NbClust)
library(clusterCrit)
library(fpc)
library(factoextra)


c <-read.csv("dataset.csv",header = T,encoding="UTF-8") 
c2 <- c[,2:3]#Select columns for clustering

#normalization of dataset variables

norm=(c2-min(c2))/(max(c2)-min(c2))

#The function returns internal indexes to Fanny Algorithm

x=c(1.5, 1.8) #Fuzzifier index values

for(i in x){

intern <- clValid(norm, 2:3, clMethods=c("fanny"), validation="internal", maxitems=600, metric="euclidean", memb.exp=1.5)
summary(intern)

}

#Nbclust k-means

results <- NbClust(data=norm, distance="euclidean", min.nc=2, max.nc=10, method="kmeans", index="dunn")
results

#K-means - new parameters

x=c(10, 20, 25) #Values for centroids initialization

for(i in x){
  
  print(i)
  km <- kmeans(norm, 4, iter.max=100, nstart = i)
  
  diss <- daisy(norm)
  
  sk <- silhouette(km$cluster, diss)
  
  #Plot for silhouette index values
  fviz_silhouette(sk)
  
}

#Identification of cluster features
c2$cluster <- km$cluster

for (i in 1:4){
  
  #Assign cluster 1 to data_clus1, cluster 2 to data_clus2, and so on...
  assign(paste0("data_clus",i), c2[c2$cluster==i,])
  #data_clus1 
}


#Multisom algorithm returns the optimal number of clusters for each SOM layer 

res <- multisom.batch(norm, xheight = 7, xwidth = 7, "hexagonal", min.radius=0.00010, 
                      max.radius=0.002, maxit = 1000, radius.type = "gaussian", alpha=1, init="random", "dunn")

res

