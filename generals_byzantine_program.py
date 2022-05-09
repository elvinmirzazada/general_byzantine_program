import sys
import random

class Node:
    def __init__(self, id):
        self.id = id
        self.name = f'G{id}'
        self.state = 'NF'
        self.main = id == 1
        self.majorities = []

    def majority(self):
        com1 = 0
        com2 = 0
        for maj in self.majorities:
            if maj == 'attack':
                com1 += 1
            else:
                com2 += 1
        if com1 > com2:
            return 'attack'
        elif com1 < com2:
            return 'retreat'
        else:
            return 'undefined'


    def send(self, majority):
        if self.state == 'F':
            majority = random.choice(['attack', 'retreat'])

        for node in nodes:
            if node.id != self.id and not node.main:         
                node.majorities.append(majority)

            if self.main and node.main:         
                node.majorities.append(majority)


if __name__ == "__main__":
    args = sys.argv
    nodes = []

    if len(args) > 1:
        n_nodes = int(args[1])            
        if(n_nodes == 0):
            print("Number of nodes can not be zero!!! Please use only integers!")
        else:                
            for i in range(1, n_nodes+1):
                node = Node(i)
                nodes.append(node)

    # start the main loop
    running = True

    while running:
        input_ = input("\nEnter command: ").lower()
        cmd = input_.split(" ")

        command = cmd[0]
        arg = cmd[1] if len(cmd) > 1 else None

        if len(cmd) > 3:
            print("Too many arguments")

        # handle actual-order
        elif command == "actual-order":
            faulty_nodes = []
            for node in nodes:
                if node.state == 'F':
                    faulty_nodes.append(node)

            faulty_state_count = len(faulty_nodes)
            all_nodes_count = len(nodes)
            q_count = all_nodes_count // 2 + 1
            define_test = 3 * faulty_state_count + 1 <= all_nodes_count

            for n in nodes:
                n.send(arg)

            for n in nodes:
                role = 'primary' if n.main else 'secondary'
                print(f"{n.name}, {role}, marjority = {n.majority()}, state={n.state}")

            if define_test:
                state_majority = f'{faulty_state_count} faulty' if faulty_state_count > 0 else 'Non-faulty'
                print(f'Execute order: {arg}! {state_majority} nodes in the system – {q_count} out of {all_nodes_count} quorum suggest {arg}')
            else:
                print("Execute order: cannot be determined – not enough generals in the system! " + 
                    f"{faulty_state_count} faulty node in the system - {q_count} out of {all_nodes_count} quorum not consistent")

            for n in nodes:
                n.majorities = []
        
        # handle g-state
        elif command == "g-state":
            if arg is None:
                for n in nodes:
                    role = 'primary' if n.main else 'secondary'
                    print(f"{n.name}, {role}, state={n.state}")
            else:
                id = int(arg)
                state = cmd[2]
                for n in nodes:
                    if n.id == id:
                        n.state = 'F' if state == 'faulty' else 'NF'
                for n in nodes:
                    role = 'primary' if n.main else 'secondary'
                    print(f"{n.name}, {role}, state={n.state}")

        # handle g-kill
        elif command == "g-kill":
            id = int(arg)
            new_node_list = []
            is_main_deleted = False
            for n in nodes:
                if n.id == id:
                    is_main_deleted = n.main
                else:
                    if is_main_deleted:
                        n.main = True
                        is_main_deleted = False
                    new_node_list.append(n)

            nodes = new_node_list
            for n in nodes:
                print(f"{n.name}, state={n.state}")

        # handle g-add
        elif command == "g-add":
            len_new_nodes = int(arg)
            last_id = nodes[-1].id+1
            print(last_id)
            for i in range(last_id, len_new_nodes+last_id):
                nodes.append(Node(i))
            for n in nodes:
                print(f"{n.name}, state={n.state}")
            

        # handle exit
        elif command == "exit":
            running = False

        # handle unsupported command        
        else:
            print("Unsupported command!:", input_)

    print("Program exited!!!")