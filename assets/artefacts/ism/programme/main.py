from context import AttackTree, MermaidPlotter, multiple_chances, yes_or_no

def read_STIX(*args, **kwargs):
    '''Get STIX Filepath'''
    datapath = input(f"Please provide a filepath to threat data: \n")
    at = AttackTree(datapath)
    print("The STIX data has been read.")
    return at

def user_option(*args, **kwargs):
    '''Get action choice off user'''
    # Show options
    options = [
        "1. Draw the Attack Tree",
        "2. Tag a keyword and value to a node",
        "3. Aggregate child node values",
        "4. Exit"
    ]
    print(f"What would you like to do? \n")
    for option in options:
        print(option)
    # Get selection
    selection = input(f"Please provide a selection: [{1}-{len(options)}]: \n")
    # Intepret selection
    action_map = {
        1 : draw_tree,
        2 : add,
        3 : aggregate,
        4 : False
    }
    action = action_map[int(selection)]
    return action

def draw_tree(at, *args, **kwargs):
    '''Draw the attack tree'''
    # Diagram configuration
    filename = input(f"Please provide a filename for the attack tree visualisation: \n")
    if yes_or_no("Would you like to view a specific tag?"):
        detail = input(f"Please enter a tag keyword: \n")
    else:
        detail = ""
    # Diagram production
    plotter = MermaidPlotter()
    plotter.plot_attack_tree(filename, at, detail)
    print("The visualisation has been created.")
    return True

def add(at, *args, **kwargs):
    node_id = input(f"Please provide the name of the node to add a tag too: \n")
    detail = input(f"Please enter a tag keyword: \n")
    value = input(f"Please enter a tag value: \n")
    at.add_value_to_node(node_id, detail, value)
    return True

def aggregate(at, *args, **kwargs):
    node_id = input(f"Please provide the name of the node to add a tag too: \n")
    detail = input(f"Please enter a tag keyword: \n")
    at.add_value_to_node(node_id, detail, value=False, aggregate=True)
    return True


def exit_script():
    pass


if __name__ == "__main__":
    if attack_tree := multiple_chances(read_STIX):
        while action := multiple_chances(user_option):
            multiple_chances(action, attack_tree)
            if yes_or_no("Would you like to do something else?") == False:
                break
    exit_script()
    