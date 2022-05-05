import numpy as np
import pandas as pd

class DomainIdentification():
    def __init__(self):
        """
        Domain identification class initialization functions
        loads the distance matrix and nodes
        """
        # Distance Matrix extracted from research paper for calculating distance between nodes
        self.distance_matrix = pd.read_csv("./distance_matrix.csv", header=None).to_numpy()

        # Empty dictionary of nodes
        self.nodes = dict()
    
    def cal_distance(self, node, parent_node):
        """
        calculates the distance between current node and parent node
        Parameters:
        node: Current node
        parent_node: Node which is calling this function
        """
        return self.distance_matrix[node-1][parent_node-1]

    def create_domain_initials(self, processing_element):
        """
        Generate the initial domains with respect to processing element
        Parameter:
        processing_element: User entered parent node
        """
        for node in self.nodes.keys():
            if not self.nodes[node]['processing_element'] and self.cal_distance(self.nodes[node]['node_id'], processing_element) <=5:
                self.nodes[node]['domain_initial'] = True
                self.nodes[node]['connected'] = True
                self.nodes[node]['visited'] = True
                self.nodes[processing_element]['domain_nodes'].append(self.nodes[node]['node_id'])
                self.nodes[processing_element]['connected'] = True

    def main(self):
        # Enter the number of required no of nodes, if 15 nodes are entered, they will be ordered from 0 to 14
        num_nodes = int(input("Enter no of nodes: "))

        # Initializing nodes
        for i in range(1, num_nodes+1, 1):
            self.nodes[i] = {
                'node_id': i,
                'processing_element': False,
                'domain_initial': False,
                'connected': False,
                'domain_nodes': [],
                'visited': False
            }

        # Creating primary node and initiating the graph building process
        processing_element = int(input("Enter processing element/ node number: "))
        self.nodes[processing_element]['processing_element'] = True
        self.nodes[processing_element]['visited'] = True

        self.create_domain_initials(processing_element)
        
        flg = False
        while(not flg):
            remaining_nodes = [self.nodes[node]['node_id'] for node in self.nodes.keys() if self.nodes[node]['connected']==False]
            domain_initials = [self.nodes[node]['node_id'] for node in self.nodes.keys() if self.nodes[node]['domain_initial']==True]
            
            # print("Nodes: ", self.nodes)
            closest_mapping = {remain: [] for remain in remaining_nodes}
            for remain in remaining_nodes:
                for di in domain_initials:
                    if self.cal_distance(remain, di) <= 5:
                        closest_mapping[remain].append(di)
            # print("closest mapping: ", closest_mapping)
            # print("remaining_nodes: ", remaining_nodes)
            membership_value = {di: {} for di in domain_initials}
            
            for remain in remaining_nodes:
                dist = {}
                for di in closest_mapping[remain]:
                    dist[di] = self.cal_distance(remain, di)
                # print("dist: ", dist)
                denom = 0
                for di in closest_mapping[remain]:
                    denom = denom + 1/ dist[di]
                # print("denom: ", denom)
                for di in domain_initials:
                    if di in closest_mapping[remain] and denom != 0:
                        membership_value[di][remain] = round((1/ dist[di])/ denom, 2)
                    else:
                        membership_value[di][remain] = 0
                # print("membership_value: ", membership_value)    
            # print("membership_value: ", membership_value)

            di_loads = {}
            for di in domain_initials:
                load = 0
                for remain in remaining_nodes:
                    load += membership_value[di][remain]
                di_loads[di] = round(load, 2)
            # print("di_loads: ", di_loads)

            sort_remaining_nodes = sorted(closest_mapping.items(), key=lambda x: len(x[1]), reverse=False)
            sorted_remaining_nodes = {}
            for i, j in sort_remaining_nodes:
                sorted_remaining_nodes[i] = j
            # print(sorted_remaining_nodes)

            for i in sorted_remaining_nodes.keys():
                if len(sorted_remaining_nodes[i]) <= 0:
                    continue
                elif len(sorted_remaining_nodes[i]) == 1:
                    self.nodes[sorted_remaining_nodes[i][0]]['domain_nodes'].append(i)
                    self.nodes[sorted_remaining_nodes[i][0]]['domain_initial'] = False
                    self.nodes[i]['connected'] = True
                    self.nodes[i]['domain_initial'] = True
                    self.nodes[i]['visited'] = True
                elif len(sorted_remaining_nodes[i]) > 1:
                    max_parent = -1
                    max_parent_val = -1
                    for j in sorted_remaining_nodes[i]:
                        if membership_value[j][i] > max_parent_val:
                            max_parent = j
                            max_parent_val = membership_value[j][i]
                    self.nodes[max_parent]['domain_nodes'].append(i)
                    self.nodes[max_parent]['domain_initial'] = False
                    self.nodes[i]['connected'] = True
                    self.nodes[i]['domain_initial'] = True
                    self.nodes[i]['visited'] = True
                    for j in sorted_remaining_nodes[i]:
                        if j != max_parent:
                            di_loads[j] = round(di_loads[j] - membership_value[j][i],2)
            
            for node in self.nodes.keys():
                if node in domain_initials and len(self.nodes[node]['domain_nodes']) < 2:
                    self.nodes[node]['connected'] = False
                    self.nodes[node]['domain_initial'] = False
                    # self.nodes[node]['visited'] = False
                    for di in self.nodes[node]['domain_nodes']:
                        self.nodes[di]['connected'] = False
                        self.nodes[di]['domain_initial'] = False
                        # self.nodes[node]['visited'] = False
                    self.nodes[node]['domain_nodes'].clear()

            for node in self.nodes.keys():
                if self.nodes[node]['domain_initial'] == False and self.nodes[node]['connected'] == False:
                    flg = False
                    break
                else:
                    flg=True
        
        print("Nodes: ", self.nodes)
        for node in self.nodes.keys():
            print("{}:  {}".format(node, self.nodes[node]['domain_nodes']))
        print()
        print("di_loads: ", di_loads)

        return None

if __name__ == '__main__':
    domain_id = DomainIdentification()
    domain_id.main()