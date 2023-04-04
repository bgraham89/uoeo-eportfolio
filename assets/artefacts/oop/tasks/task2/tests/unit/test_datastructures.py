'''Unit tests for guard helper functions'''

from context import datastructures as avds
from context import encoders as enc
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
        new_address = enc.int_to_array(self.senders_address, self.md_size)
        package.update_address(new_address)
        postupdate = list(package.read_meta_data())
        self.assertNotEqual(preupdate, postupdate)


if __name__ == '__main__':
    unittest.main()