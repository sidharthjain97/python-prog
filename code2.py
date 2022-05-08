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
        self.closest_mapping, self.membership_value, self.di_loads = {}, {}, {}
    
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
                self.nodes[node]['visited'] = 1
                self.nodes[node]['parent'].append(processing_element)
                self.nodes[processing_element]['domain_nodes'].append(self.nodes[node]['node_id'])
                self.nodes[processing_element]['connected'] = True

    def find_closest_mapping(self, domain_initials, remaining_nodes):
        self.closest_mapping = {remain: [] for remain in remaining_nodes}
        for remain in remaining_nodes:
            for di in domain_initials:
                if self.cal_distance(remain, di) <= 5:
                    self.closest_mapping[remain].append(di)

    def find_membership_value(self, domain_initials, remaining_nodes):
        self.membership_value = {di: {} for di in domain_initials}
        
        for remain in remaining_nodes:
            dist = {}
            for di in self.closest_mapping[remain]:
                dist[di] = self.cal_distance(remain, di)
            # print("dist: ", dist)
            denom = 0
            for di in self.closest_mapping[remain]:
                denom = denom + 1/ dist[di]
            # print("denom: ", denom)
            for di in domain_initials:
                if di in self.closest_mapping[remain] and denom != 0:
                    self.membership_value[di][remain] = round((1/ dist[di])/ denom, 2)
                else:
                    self.membership_value[di][remain] = 0

    def cal_di_loads(self, domain_initials, remaining_nodes, processing_element):
        # print("di_loads before: ",self.di_loads)
        for di in domain_initials:
            ori = di
            # print("ori: ", ori)
            p = self.nodes[di]['parent'][0]
            while(p != processing_element):
                di = p
                p = self.nodes[p]['parent'][0]
            # print("P: ", p)
            # print("di: ", di)
            load = self.di_loads[di]
            for remain in remaining_nodes:
                load += self.membership_value[ori][remain]
            self.di_loads[di] = round(load, 2)

    def attach_nodes(self, processing_element):
        # print("self.membership_value: ",self.membership_value)
        sort_remaining_nodes = sorted(self.closest_mapping.items(), key=lambda x: len(x[1]), reverse=False)
        # print("sort_remaining_nodes: ", sort_remaining_nodes)
        sorted_remaining_nodes = {}
        for i, j in sort_remaining_nodes:
            sorted_remaining_nodes[i] = j
        # print("sorted_remaining_nodes: ",sorted_remaining_nodes)

        for i in sorted_remaining_nodes.keys():
            if len(sorted_remaining_nodes[i]) <= 0:
                continue
            elif len(sorted_remaining_nodes[i]) == 1:
                self.nodes[sorted_remaining_nodes[i][0]]['domain_nodes'].append(i)
                self.nodes[sorted_remaining_nodes[i][0]]['domain_initial'] = False
                self.nodes[i]['connected'] = True
                self.nodes[i]['domain_initial'] = True
                self.nodes[i]['parent'].append(sorted_remaining_nodes[i][0])
                self.nodes[i]['visited'] = 1
                self.nodes[i]['level'] = self.nodes[sorted_remaining_nodes[i][0]]['level'] + 1
            elif len(sorted_remaining_nodes[i]) > 1:
                max_parent = -1
                max_parent_val = -1
                for j in sorted_remaining_nodes[i]:
                    # print("j: ", j)
                    if self.membership_value[j][i] > max_parent_val:
                        max_parent = j
                        max_parent_val = self.membership_value[j][i]
                # print("max_parent:", max_parent)
                # print("max_parent_val:", max_parent_val)
                self.nodes[max_parent]['domain_nodes'].append(i)
                self.nodes[max_parent]['domain_initial'] = False
                self.nodes[i]['connected'] = True
                self.nodes[i]['domain_initial'] = True
                self.nodes[i]['parent'].append(max_parent)
                self.nodes[i]['visited'] = 1
                self.nodes[i]['level'] = self.nodes[max_parent]['level'] + 1
                for j in sorted_remaining_nodes[i]:
                    # print("j: ", j)
                    ori = j
                    p = self.nodes[j]['parent'][0]
                    while(p != processing_element):
                        j = p
                        p = self.nodes[p]['parent'][0]
                    if ori != max_parent:
                        self.di_loads[j] = round(self.di_loads[j] - self.membership_value[ori][i],2)

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
                'parent': [],
                'domain_nodes': [],
                'visited': 0,
                'level': 0
            }

        # Creating primary node and initiating the graph building process
        processing_element = int(input("Enter processing element/ node number: "))
        self.nodes[processing_element]['processing_element'] = True
        self.nodes[processing_element]['visited'] = 1

        self.create_domain_initials(processing_element)
        domain_initials1 = [self.nodes[node]['node_id'] for node in self.nodes.keys() if self.nodes[node]['domain_initial']==True]
        self.di_loads = {key: 0 for key in domain_initials1}

        flg = False
        while(not flg):
            remaining_nodes = [self.nodes[node]['node_id'] for node in self.nodes.keys() if self.nodes[node]['connected']==False and self.nodes[node]['domain_initial'] == False]
            domain_initials = [self.nodes[node]['node_id'] for node in self.nodes.keys() if self.nodes[node]['domain_initial']==True]
            # print("remaining_nodes: ", remaining_nodes)
            # print("domain_initials: ", domain_initials)
            
            # print("Nodes: ", self.nodes)
            self.find_closest_mapping(domain_initials, remaining_nodes)
            # print("closest mapping: ", self.closest_mapping)
            
            self.find_membership_value(domain_initials, remaining_nodes)
            # print("membership_value: ", self.membership_value)

            
            self.cal_di_loads(domain_initials, remaining_nodes, processing_element)
            
            self.attach_nodes(processing_element)
            # print("after 1st attaching nodes di_loads: ", self.di_loads)
            # print("di_loads: ", self.di_loads)

            for node in self.nodes.keys():
                if self.nodes[node]['level'] == 0 and len(self.nodes[node]['domain_nodes']) < 2 and node in domain_initials1:
                    self.nodes[processing_element]['domain_nodes'].remove(node)
                    if node in self.di_loads.keys():
                        del self.di_loads[node]
                    self.nodes[node]['connected'] = False
                    self.nodes[node]['domain_initial'] = False
                    self.nodes[node]['visited'] = 0
                    self.nodes[node]['parent'].clear()
                    for dn in self.nodes[node]['domain_nodes']:
                        self.nodes[dn]['connected'] = False
                        self.nodes[dn]['domain_initial'] = False
                        self.nodes[dn]['parent'].clear()
                        self.nodes[dn]['visited'] = 0
                    self.nodes[node]['domain_nodes'].clear()

            flg = self.nodes[processing_element]['visited']
            for node in self.nodes.keys():
                if node in domain_initials:
                    if self.nodes[node]['domain_initial'] == True:
                        self.nodes[node]['domain_initial'] = False
                if node != processing_element:
                    flg &= self.nodes[node]['visited']
        # print(flg)

        

        print("Nodes: ", self.nodes)
        for node in self.nodes.keys():
            print("{}:  {}".format(node, self.nodes[node]['domain_nodes']))
        # print()
        # print("self.di_loads: ", self.di_loads)

        return None

if __name__ == '__main__':
    domain_id = DomainIdentification()
    domain_id.main()