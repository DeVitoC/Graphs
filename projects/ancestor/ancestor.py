from util import Queue

def earliest_ancestor(ancestors, starting_node):
    # Create queue for short term storage of nodes to test
    queue = Queue()
    current_node = starting_node
    paths = {}

    # Create dictionary of relationships with the children as the keys and parents as the values
    relationships = {}
    for node in ancestors:
        if node[1] not in relationships:
            relationships[node[1]] = set()
        relationships[node[1]].add(node[0])

    # Test if the node given is a key (child) in the relationships dictionary
    if starting_node in relationships:
        queue.enqueue(relationships[current_node])
    # If not, return -1
    else:
        return -1

    # Loop until topmost parent has been found
    while True:
        # Dequeue set of parents for node (initially starting_node, subsequently, lowest id parent)
        relations = queue.dequeue()
        # Set current_node to lowest ID of parents
        current_node = min(relations)
        # If lowest ID parent not in dictionary (i.e. not a child of any parents) return node
        if current_node not in relationships:
            return current_node
        # Else, queue up the parents of current_node
        else:
            queue.enqueue(relationships[current_node])

