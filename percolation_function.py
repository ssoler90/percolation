import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

"""
 We create a network of (N+2)x(N+2) and we fill the first and last column and row with zeros
 and the rest that is the NxN network with zeros and ones according to the probability value. 
 It is done this way so that the "clusterization" algorithm defined below works correctly.
"""
def net(size_net, probability):
        net = np.random.random((size_net + 2,size_net +2))
        net = (net < probability)
        net[:,0] = 0
        net[:,size_net + 1] = 0
        net[0,:] = 0
        net[size_net + 1, :] = 0
        return net*1
    
"""
The "clusterization" algorithm works as follows: when we find a cell[i,j]
 that has the value 1 we add it to the "count_cluster" array and give it 
 the corresponding cluster label. Now we check if the cell has any nearest neighbors 
 with the value 1, that is, cell[i+1,j], cell[i-1,j], cell[i,j+1], cell[i,j-1 ], 
 once all neighboring cells have been added, we remove cell[i,j]
 from the "count_cluster" array. The process is repeated with all cells found, 
 that is, we assign the value "label_cluster" to it,
 add the neighbors of value 1 in "count_cluster" and then the given cell is removed
 from "count_cluster". Once the "count_luster" array has no elements, it means 
 that we have already found all the elements of the studied cluster, 
 so we exit the cycle and increase the value of "label _cluster" by one unit and repeat 
 the process until all the elements of matrix have been checked.    
"""
def clusterization(net):
        # We are going to count the clusters of the net_clust
        count_cluster = np.array([[0,0]])
        label_cluster = 2
        net_clust = net.copy()

        for i in range( net_clust.shape[0] -1):
            for j in range(net_clust.shape[0] -1):
                if net_clust[i+1,j+1] == 1:
                    net_clust[i+1,j+1] = label_cluster
                    count_cluster = np.vstack([count_cluster, np.array([i+1,j+1])])
                    a = True
                    while a:
                        if net_clust[count_cluster[1,0],count_cluster[1,1] - 1] == 1:
                            net_clust[count_cluster[1,0],count_cluster[1,1] - 1] = label_cluster                               
                            count_cluster = np.vstack([count_cluster,np.array([count_cluster[1,0],count_cluster[1,1] - 1])])
                        if net_clust[count_cluster[1,0],count_cluster[1,1] + 1] == 1:
                            net_clust[count_cluster[1,0],count_cluster[1,1] + 1] = label_cluster
                            count_cluster = np.vstack([count_cluster,np.array([count_cluster[1,0],count_cluster[1,1] + 1])])    
                        if net_clust[count_cluster[1,0] + 1,count_cluster[1,1]] == 1:
                            net_clust[count_cluster[1,0] + 1,count_cluster[1,1]] = label_cluster
                            count_cluster = np.vstack([ count_cluster,np.array([count_cluster[1,0] + 1,count_cluster[1,1]])])
                        if net_clust[count_cluster[1,0] - 1,count_cluster[1,1]] == 1:
                            net_clust[count_cluster[1,0] - 1,count_cluster[1,1]] = label_cluster                               
                            count_cluster = np.vstack([ count_cluster,np.array([count_cluster[1,0] - 1,count_cluster[1,1]])])

                        count_cluster = np.delete(count_cluster, 1, axis = 0)

                        if count_cluster.size == 2:
                            a = False
                            label_cluster = label_cluster + 1
        return net_clust

# We create the class percolation to find if there is precolation in the given net  
class Percolation:
    def __init__(self, size_net, probability):
        self.size_net = size_net
        self.probability = probability
        self.net = net(size_net, probability)
        self.net_clust = clusterization(self.net)
        
    def is_percolation(self):
        first_row = self.net_clust[1,:][self.net_clust[1,:]>0]
        last_row = self.net_clust[self.size_net,:][self.net_clust[self.size_net,:]>0]
        is_percolation = np.any(first_row.reshape(np.size(first_row),1) == last_row)
        return is_percolation

