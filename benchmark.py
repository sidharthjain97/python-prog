import pandas as pd

distance_matrix = pd.read_csv("./distance_matrix.csv", header=None).to_numpy()

def cal_distance(self, node, parent_node):
    """
    calculates the distance between current node and parent node
    Parameters:
    node: Current node
    parent_node: Node which is calling this function
    """
    return self.distance_matrix[node-1][parent_node-1]

def kmeans():
    centroids = [4,7,14]
    return None

if __name__=="__main__":
    pass