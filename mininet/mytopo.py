from mininet.topo import Topo

item_map = {}   # maps switch and host name to objects 
adj_list_1 = {
            's1':['s2','s3','h1','h2'],
            's2':['s4','h3','h4'],
            's3':['s5','h5','h6'],
            's4':['s5','h7','h8'],
            's5':['h9','h10']
}

adj_list_2 = {
            's1':['s2','s3','h1','h2'],
            's2':['s4','h3','h4'],
            's3':['s4','s5','h5','h6'],
            's4':['s5','h7','h8'],
            's5':['h9','h10']
}

adj_list=adj_list_2

class MyTopo(Topo ):
    def build( self ):
        # builds topology from the adj_list definition 
        for switch in adj_list:
            print(f'\t switch {switch} added')
            item_map[switch] = self.addSwitch(switch)
            print(f'\t switch {switch} added')
            for item in adj_list[switch]:
                if item[0] == 's' and item not in item_map:
                    item_map[item] = self.addSwitch(item)
                    print(f'\t\t switch {item} added')
                elif item[0] == 'h' and item not in item_map:
                    item_map[item] = self.addHost(item)
                    print(f'\t\t host {item} added')
                
                self.addLink(item_map[switch], item_map[item])
                print(f'\t\t link ( {switch}, {item}) added')

topos = { 'mytopo': ( lambda: MyTopo() ) }
