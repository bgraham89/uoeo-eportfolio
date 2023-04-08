'''Unit tests for guard helper functions'''

from context import datastructures as avds
from context import converters as conv
from context import protocols
import unittest

class TestFixedArray(unittest.TestCase):
    '''Unit tests for the FixedArray class.'''

    def setUp(self):
        self.size = 10
        self.data = ["d", "u", "m", "m", "y", "", "d", "a", "t", "a"]
        self.step = 2

    def test_size_assigned(self):
        '''Expect size attribute to match input.'''
        fixed_array = avds.FixedArray(self.size)
        self.assertEqual(len(fixed_array), self.size)

    def test_size_rejected(self):
        '''Expect bad size to raise AssertionError.'''
        with self.assertRaises(AssertionError):
            avds.FixedArray(-1 * self.size)

    def test_index_constraints_passed(self):
        '''Expect good index to pass constraint check.'''
        fixed_array = avds.FixedArray(self.size)
        func = fixed_array._index_constraints
        self.assertTrue(func()(self.size - 1))

    def test_index_constraints_failed(self):
        '''Expect bad index to fail constraint check.'''
        fixed_array = avds.FixedArray(self.size)
        func = fixed_array._index_constraints
        self.assertFalse(func()(self.size))

    def test_data_constraints_passed(self):
        '''Expect good data to pass constraint check.'''
        fixed_array = avds.FixedArray(self.size)
        func = fixed_array._data_constraints
        self.assertTrue(func()(self.data))

    def test_data_constraints_failed(self):
        '''Expect good data to fail constraint check.'''
        fixed_array = avds.FixedArray(self.size)
        func = fixed_array._data_constraints
        self.assertFalse(func()(self.data + ["!"]))

    def test_upgradable(self):
        '''Expect list attribute to be updated.'''
        fixed_array = avds.FixedArray(self.size)
        fixed_array.update(self.data)
        self.assertEqual(list(fixed_array), self.data)

    def test_upgrade_rejected(self):
        '''Expect upgrade to raise AssertionError.'''
        fixed_array = avds.FixedArray(self.size)
        with self.assertRaises(AssertionError):
            fixed_array.update(self.data + ["!"])
    
    def test_indexable(self):
        '''Expect FixedArray items match data items.'''
        fixed_array = avds.FixedArray(self.size)
        fixed_array.update(self.data)
        for i in range(self.size):
            self.assertEqual(fixed_array[i], self.data[i])
    
    def test_slicable(self):
        '''Expect FixedArray slices match data slices.'''
        fixed_array = avds.FixedArray(self.size)
        fixed_array.update(self.data)
        for i in range(self.size):
            self.assertEqual(fixed_array[i:], self.data[i:])
            self.assertEqual(fixed_array[:i], self.data[:i])
        self.assertEqual(fixed_array[::self.step], self.data[::self.step])


class TestPackage(unittest.TestCase):
    '''Unit tests for the Package class.'''

    def setUp(self):
        self.data = ["d", "u", "m", "m", "y", "", "d", "a", "t", "a"] * 10
        self.tags = ("this", "last", "address", "op")
        self.meta_data = {"this" : 1,"last" : 1, "address" : 1, "op" : 1}
        self.head_size = 32
        self.md_size = 8
        self.body_size = 64
        self.senders_address = 255

    def test_size_assigned(self):
        '''Expect size attribute to match input.'''
        package = avds.Package(self.head_size, self.body_size)
        self.assertEqual(len(package.read_meta_data()), self.head_size)
        self.assertEqual(len(package.read_data()), self.body_size)
        self.assertEqual(len(package), self.body_size + self.head_size)

    def test_size_rejected(self):
        '''Expect bad size to raise AssertionError.'''
        with self.assertRaises(AssertionError):
            avds.Package(-1 * self.head_size, self.body_size)

    def test_meta_data_packer(self):
        '''Test meta data dictionary packed into an array.'''
        package = avds.Package.Basic(self.data[:32], self.meta_data)
        self.assertTrue(package.pack_meta_data(self.meta_data, self.tags, self.md_size))
 
    def test_md_constraints_passed(self):
        '''Expect good metadata values to pass constraint check.'''
        package = avds.Package(self.head_size, self.body_size)
        func = package._md_constraints
        self.assertTrue(func(self.md_size)(self.meta_data["this"],))

    def test_md_constraints_failed(self):
        '''Expect bad metadata to fail constraint check.'''
        package = avds.Package(self.head_size, self.body_size)
        func = package._md_constraints
        self.meta_data.update({"this" : 2 ** self.md_size})
        self.assertFalse(func(self.md_size)(self.meta_data["this"],))

    def test_basic_package_stores_data(self):
        '''Expect data attributes to be updated correctly.'''
        package = avds.Package.Basic(self.data[:32], self.meta_data)
        self.assertTrue(package.read_data(), self.data[:32])

    def test_basic_package_packs_data(self):
        '''Expect data attributes to be updated correctly.'''
        package = avds.Package.Basic(self.data[:31], self.meta_data)
        self.assertTrue(package.read_data(), self.data[:31]+["0"])

    def test_basic_package_stores_meta_data(self):
        '''Expect attributes to be updated correctly.'''
        package = avds.Package.Basic(self.data[:32], self.meta_data)
        meta_data = self.meta_data
        tags = protocols.Basic.TAGS
        charlimit = protocols.Basic.HEAD_SEGMENT_SIZE
        package.pack_meta_data(meta_data, tags, charlimit)
        self.assertTrue(package.read_meta_data())

    def test_updateable_address(self):
        '''Expect header gets updates'''
        package = avds.Package.Basic(self.data[:32], self.meta_data)
        preupdate = list(package.read_meta_data())
        new_address = conv.int_to_array(self.senders_address, self.md_size)
        package.update_address(new_address)
        postupdate = list(package.read_meta_data())
        self.assertNotEqual(preupdate, postupdate)

class TestGraph(unittest.TestCase):
    '''Unit tests for the Graph class.'''

    def setUp(self):
        self.nodes = [n for n in range(20)]
        self.badnodes = [[n] for n in range(20)]
        self.edges = [(n, n+1) for n in range(19)]
        self.badedges = [(n, n+1) for n in range(20)]

    def test_nodes_assigned(self):
        '''Expect nodes attribute to match input.'''
        graph = avds.Graph()
        graph.add_nodes(self.nodes)
        self.assertEqual(graph._nodes, set(self.nodes))

    def test_good_nodes_assigned(self):
        '''Expect nodes attribute to match input.'''
        graph = avds.Graph()
        graph.add_nodes(self.nodes)
        self.assertEqual(graph._nodes, set(self.nodes))

    def test_bad_nodes_not_assigned(self):
        '''Expect bad nodes to raise AssertionError'''
        graph = avds.Graph()
        with self.assertRaises(AssertionError):
            graph.add_nodes(self.badnodes)

    def test_good_edges_assigned(self):
        '''Expect good edges attribute to match input.'''
        graph = avds.Graph()
        graph.add_nodes(self.nodes)
        for a, b in self.edges:
            graph.add_directed_edge(a, b)
            self.assertTrue(b in graph._edges[a])

    def test_bad_edges_not_assigned(self):
        '''Expect bad edges to raise AssertionError'''
        graph = avds.Graph()
        graph.add_nodes(self.nodes)
        with self.assertRaises(AssertionError):
            graph.add_directed_edge(*self.badedges[-1])

    def test_directed_edge_is_one_way(self):
        '''Expect oppoiste edge not in graph'''
        graph = avds.Graph()
        graph.add_nodes(self.nodes)
        graph.add_directed_edge(*self.edges[0])
        self.assertTrue(self.edges[0][1] not in graph._edges)

    def test_edge_is_undirected(self):
        '''Expect opposite edge in graph'''
        graph = avds.Graph()
        graph.add_nodes(self.nodes)
        node_i, node_ii = self.edges[0]
        graph.add_undirected_edge(node_i, node_ii)
        self.assertTrue(node_i in graph._edges[node_ii])

    def test_null_graph_has_nodes(self):
        '''Expect nodes in graph'''
        graph = avds.Graph.Null(self.nodes)
        self.assertTrue(graph._nodes, set(self.nodes))

    def test_null_graph_has_no_edges(self):
        '''Expect no edges in graph'''
        graph = avds.Graph.Null(self.nodes)
        self.assertTrue(len(graph._edges) == 0)


if __name__ == '__main__':
    unittest.main()