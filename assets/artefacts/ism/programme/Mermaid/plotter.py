class MermaidPlotter(object):
    def __init__(self, output_path="./diagrams/"):
        self._output_path = output_path

    @property
    def output_path(self):
        return self._output_path

    @output_path.setter
    def output_path(self, output_path):
        self._output_path = output_path

    def plot_attack_tree(self, filename, attack_tree, detail=""):
        with open(self._output_path + filename + ".md", "w") as file:
            file.write(f"# Attack Tree\n\n")
            file.write(f"```mermaid\ngraph LR;\n")
            self.add_relationships(file, attack_tree.root_node, detail)
            file.write("```\n")
    
    def add_relationships(self, file, node, detail):
        '''Adds edges to flow diagram'''
        if node.child_nodes:
            # Create LHS of mermaid syntax
            p_obj = self.add_vertice(node, detail)
            for c in node.child_nodes.values():
                # Create RHS of mermaid syntax
                c_obj = self.add_vertice(c, detail)
                # Add new line to file
                file.write(f"  {p_obj} --- {c_obj};\n")
                # Check for child nodes of child node
                self.add_relationships(file, c, detail)
    

    def add_vertice(self, node, detail):
        '''Adds a vertice for the flow diagram'''
        # vertice content
        has_detail = detail in node.values
        content_detail = f"{detail}: {node.values[detail]}" if has_detail else ""
        content_titled = f"\"`{node.id}" + f"\n" + content_detail + f"`\""
        # vertice shape
        if node.values["type"] == "root":
            vertice_shape = f"((({content_titled})))"
        elif node.values["type"] == "grouping":
            vertice_shape = f"(({content_titled}))"
        else:
            vertice_shape = "{{" + f"{content_titled}" + "}}"
        
        return f"{node.id.replace(' ', '')}{vertice_shape}"
    
