from context import STIXParser, Tree

if __name__ == "__main__":
    filepath = input(f"Please provide a filepath to the json: \n")
    parser = STIXParser(mode="attack_tree")
    params_array = parser(filepath)
    print("NodeParamaters created successfully")
    #print(f"node_{params_array=}")
    #print(f"{parser.data=}")
    tree_id = ""
    tree_description = "An attack tree for debugging purposes"
    tree_values = {"filepath" : filepath}
    tree = Tree(id=tree_id, description=tree_description, 
                values=tree_values, node_paramaters_array=params_array)
    print("Tree created successfully")
    print(f"{tree.id=}")
    print(f"{tree.description=}")
    print(f"{tree.values=}")
    print(f"{tree.root_node=}")
    print(f"{tree=}")