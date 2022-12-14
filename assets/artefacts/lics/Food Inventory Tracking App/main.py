# Standard Library Imports ---------------------------------


from random import choice
from time import sleep


# Global Variables -----------------------------------------


DEBUGMODE = False


# Data Structures ------------------------------------------


class HashMap(object):
  """
    A high-level implementation of a hash map, to explicity
    share associated algorithms, and demonstrate application.
    
    Attributes
    ----------    
    keys : A container object that supports .add(), .discard(), 
           and .difference() methods, conversions to a list, 
           lookups using the in keyword, and dynamic resizing.
           This stores keys associated with stored data which 
           are always of str type.

    num_buckets : An int. This tracks how many addresses of
                  storage are indexed. 

    num_empty_buckets : An int. This tracks how many addresses of 
                        storage are empty.

    num_keys : An int. This tracks how many keys are stored.
    
    storage : A container object that supports 
              indexing using integers, data mutations, 
              slicing, and concatenation with itself.
              This imitates locations in memory.

    Methods
    -------
    Hash : Converts a key into an address in storage.

    Insert : Inserts data into storage at a location determined by
             the hash of a corresponding key.

    Search : Searches for a node in storage corresponding to a key,
             from which data can be pulled.

    Delete : Deletes data in storage that corresponds to a key.

    Sort : Provides a list of keys in alphabetical order.


    Disclaimer
    ----------
    While this implementation of a hashmap is functional, 
    it is recommended to use the standard implementation
    built into python; the built-in dict datatype, which
    uses optimizations beyond the scope of this demo,
    unless a specialised type of storage data structure is
    required. 

    Furthermore, It's worth noting that any data structure 
    implemented in python code to be used for the storage 
    attribute is unlikely to be an improvement over one 
    implemented in a lower-lever language with explicit
    access to memory pointers. The built-in list data type 
    is used by default for the storage attribute,
    because its array structure is similar to that of the 
    structure of typical memory. 

    The default structure for the keys container is a set,
    which is inserted into index 0 of the storage attribute,
    so index 0 must be reserved for keys. There is no additional 
    coupling implemented, so any custom data structure coupling 
    can be handled hassle free outside of the HashMap class.
    A set structure is chosen by default for it's amortised, 
    constant-time insertions, deletions and lookups. 
  """

  def __init__(self, name, memory="default", keys_container="default"):
    """
      The constuctor of the HashMap class. 

      Parameters
      ----------
      memory : (optional) A container object that must support 
              indexing using integers, data mutations, 
              slicing, and concatenation with itself.

      name : A str to identify the hashmap

      keys_container : (optional) A container object that must
                       support .add(), .discard(), and 
                       .difference() methods, conversions to a 
                       list, lookups using the in keyword, and 
                       dynamic resizing.  
    """

    # initialise storage
    if memory == "default":
      self.storage = [""]
    else:
      self.storage = memory

    # initialise keys container
    if keys_container == "default":
      self.keys = set()
    else:
      self.keys = keys_container

    # guardians for custom data structures
    try:
      guardian = StorageAssertion()
      self.storage = guardian(self.storage)
      guardian = KeyContainerAssertion()
      self.keys = guardian(self.keys)
      if DEBUGMODE:
        str_self = str(self)
        print("[DEBUG][init][Assignment] hashmap: ", str_self)
        print("[DEBUG][init][Assignment] keys: ", self.keys)
        print("[DEBUG][init][Assignment] storage: ", self.storage)
        print("[DEBUG][init][Parameter] name: ", name)

    except Exception as e:
      raise(e)

    # store keys in storage
    self.storage += self.storage
    self.storage[0] = self.keys
    if DEBUGMODE: 
      print("[DEBUG][init][Update] storage:", self.storage)

    # initialise tracking attributes
    self.num_empty_buckets, self.num_buckets = 1, 2
    self.num_keys = 0
    if DEBUGMODE: 
      print("[DEBUG][init][Update] num_buckets: ", self.num_buckets)
      print("[DEBUG][init][Update] num_empty_keys: ", self.num_empty_buckets)
      print("[DEBUG][init][Update] num_keys: ", self.num_keys)

    # give hashmap a name
    self.Insert("name", name)
    if DEBUGMODE: 
      str_self = str(self)
      print("[DEBUG][init][Update] hashmap: ", str_self)


  def __len__(self):
    """
      Allows the use of the len() function on a HashMap object.
    """
    # return number of data keys stored
    return self.num_keys


  def __str__(self):
    """
      Allows the use of the str() function on a HashMap object, 
      used mainly in debug mode to control order of logs.
    """
    # return name of hashmap or empty string
    return f"HashMap(name={self['name'] if 'name' in self else ''})"


  def __repr__(self):
    """
      Provides a representation for the print() function used on a HashMap object.
    """
    # return name if hashmap has one
    return f"HashMap(name={self['name'] if 'name' in self else ''})"

  
  def __getitem__(self, key):
      """
        Allows the use of index notation to access data.

        Parameters
        ----------
        key : A str. A label associated with data.
      """
      if DEBUGMODE: 
        print("[DEBUG][getitem][Parameter] key: ",  key)

      # return data associated with key
      node = self.Search(key)
      return node.value if node else None


  def __contains__(self, key):
      """
        Allows the use of the 'in' keyword.

        Parameters
        ----------
        key : A str. A label associated with data.
      """
      if DEBUGMODE: 
        print("[DEBUG][contains][Parameter] key: ",  key)
        print("[DEBUG][contains][State] keys: ", self.keys)

      # return a bool depending on whether key is being tracked.
      return key in self.keys


  def Hash(self, key, num_buckets="default"):
    """
      Converts a str into a positive int that corresponds 
      to an index of storage.

      Parameters
      ----------
      key : A str. A label associated with data.
      
      num_buckets : (optional) An int. To specify a
                    hypothetical amount of addresses 
                    that can be hashed into.  
    """
    
    # get number of buckets
    if num_buckets == "default":
      num_buckets = self.num_buckets

    if DEBUGMODE:
      print("[DEBUG][Hash][Parameter] key: ", key)
      print("[DEBUG][Hash][Parameter] num_buckets: ", num_buckets)
      print("[DEBUG][Hash][State] storage: ", self.storage)

    # guardians for parameters
    try:
      guardian = KeyAssertion()
      guardian(key)
      guardian = BucketAssertion(2)
      guardian(num_buckets)
    except Exception as e:
      raise(e)

    # get product of ASCII codes of characters in string
    product = 1
    for char in key:
      product *= ord(char)
    
    # map product to bucket
    product %= num_buckets - 1
    product += 1

    # guardians for output
    try:
      guardian = BucketAssertion(1, num_buckets)
      guardian(product)
    except Exception as e:
      raise(e)

    if DEBUGMODE: 
      print("[DEBUG][Hash][Output] hash: ", product)
    return product


  def Insert(self, key, data, nested_keys=False):
    """
      Adds data to the location in storage provided by the
      .Hash(key) method.

      Parameters
      ----------
      data : Anything that's not a None type
      
      key : A str. A label associated with the data. 

      nested_keys : (optional) A sequence of strings 
                    to store data in nested HashMap objects. 

      Disclaimer
      ----------
      Grow() will slow down an insertion into the hashmap to O(n)-time,
      assuming the hashmap has n amont of keys. However, as Grow() is
      called infrequently enough, Insert() maintains amortized O(1)-time.
    """

    # guardians for parameters
    try:
      guardian = KeyAssertion()
      guardian(key)
      assert data != None
    except Exception as e:
      raise(e)

    if DEBUGMODE:
      str_data = str(data)
      print("[DEBUG][Insert][Parameter] key: ", key)
      print("[DEBUG][Insert][Parameter] data: ", str_data)
      print("[DEBUG][Insert][Parameter] nested_keys: ", nested_keys)
      print("[DEBUG][Insert][State] storage: ", self.storage)


    # read/write to keys container
    if key in self.keys:
      key_found = True
    else:
      key_found = False
      self.keys.add(key)
      self.num_keys += 1
      if DEBUGMODE:
        print("[DEBUG][Insert][Update] keys: ", self.keys)
        print("[DEBUG][Insert][Update] num_keys: ", self.num_keys)

    # get storage address from key
    address = self.Hash(key)
    if DEBUGMODE:
      print("[DEBUG][Insert][Update] address: ", address)

    # check if data needs nesting or not
    subdata = None
    if nested_keys:
      hashmap = None
      if key_found:
        # check if nested hashmap exists to insert subdata
        if DEBUGMODE:
          print("[DEBUG][Insert][State] key: ", key)
          print("[DEBUG][Insert][State] address: ", address)
        result = self.Search(key, address)
        if type(result.value) == HashMap:
          hashmap = result.value
          subdata, data = data, None
      if not hashmap:
        # otherwise create one
        memory = self.storage[:1]
        memory[0] = ""
        keys_container = self.keys.difference(self.keys)
        name = data if nested_keys[-1] == "name" else nested_keys[-1]
        hashmap = HashMap(name, memory, keys_container)
        subdata, data = data, hashmap
      if DEBUGMODE:
        str_data, str_subdata = str(data), str(subdata)
        print("[DEBUG][Insert][Update] data: ", str_data)
        print("[DEBUG][Insert][Update] subdata: ", str_subdata)

    # insertion into this hashmap
    if data != None:
      if key_found:
        # case 1: A linked list with a node for key already exists at address
        if DEBUGMODE:
          print("[DEBUG][Insert][State] key: ", key)
          print("[DEBUG][Insert][State] address: ", address)
        result = self.Search(key, address)
        result.value = data
        if DEBUGMODE:
          str_data = (result.value)
          print("[DEBUG][Insert][Update] node:", result)
          print("[DEBUG][Insert][Update] node key: ", result.key)
          print("[DEBUG][Insert][Update] node value: ", str_data)
          print("[DEBUG][Insert][Update] node next: ", result.next)
      elif self.storage[address]:
        # case 2: A linked list without a node for key already exists at address
        node = self.storage[address]
        # search for tombstone to replace
        tombstone = True
        while tombstone:
          if DEBUGMODE:
            str_data = str(node.value)
            print("[DEBUG][Insert][Loop] node:", node)
            print("[DEBUG][Insert][Loop] node key: ", node.key)
            print("[DEBUG][Insert][Loop] node value: ", str_data)
            print("[DEBUG][Insert][Loop] node next: ", node.next)
          if node.value == None:
            node.key, node.value = key, data
            if DEBUGMODE:
              str_data = str(node.value)
              print("[DEBUG][Insert][Update] node:", node)
              print("[DEBUG][Insert][Update] node key: ", node.key)
              print("[DEBUG][Insert][Update] node value: ", str_data)
              print("[DEBUG][Insert][Update] node next: ", node.next)
            break
          elif node.next:
            node = node.next
          else:
            tombstone = False 
        else:
          # otherwise create new tail
          node.next = Node(key, data)
      else:
        # case 3: No linked list already exists at address
        # so create a head
        self.storage[address] = Node(key, data)
        self.num_empty_buckets -= 1
        if DEBUGMODE:
          print("[DEBUG][Insert][Update] storage: ", self.storage)
          print("[DEBUG][Insert][Update] num_empty_buckets: ", self.num_empty_buckets)
          print("[DEBUG][Insert][State] num_buckets: ", self.num_buckets)

        # Grow storage size when its half full
        if self.num_empty_buckets < self.num_buckets // 2:
          self.Grow()

    # insertion into nested hashmap
    if subdata:
      hashmap.Insert(nested_keys[0], subdata, nested_keys[1:])
    if DEBUGMODE:
      print("[DEBUG][Insert][End] key: ", key)

  
  def Search(self, key, address=False):
    """
      Returns node labelled by key, or None.

      Parameters
      ----------
      address : (optional) An int. The address where the  
                key is supposed to hash too. When an address
                is provided, hashing of the key is skipped.

      key : A str. A label associated with data. 
    """

    # guardians for parameters
    try:
      guardian = KeyAssertion()
      guardian(key)
      if not address:
        address = self.Hash(key)
      guardian = BucketAssertion(1, self.num_buckets)
      guardian(address)
    except Exception as e:
      raise(e)

    if DEBUGMODE:
      print("[DEBUG][Search][Parameters] key: ", key) 
      print("[DEBUG][Search][Parameters] address: ", address)
      print("[DEBUG][Search][State] storage:", self.storage)
      print("[DEBUG][Search][State] keys:", self.keys)

    # check key container
    if key not in self.keys:
      return None

    # search linked list at address for corresponding data
    node = self.storage[address]

    while node:
      if DEBUGMODE:
        str_data = str(node.value)
        print("[DEBUG][Search][Loop] node: ", node)
        print("[DEBUG][Search][Loop] node key: ", node.key) 
        print("[DEBUG][Search][Loop] node value: ", str_data)
        print("[DEBUG][Search][Loop] node next: ", node.next)
      if node.key == key:
        # case 1: found corresponding data
        return node 
      elif node.next:
        # case 2: didnt find anything, trying next node
        node = node.next
      else:
        # case 3: didnt find anything, but tail reached
        return None

  
  def Delete(self, key, address=False):
    """
      Deletes the data corresponding to a key.

      Parameters
      ----------
      key : A str. A label associated with data.

      address : (optional) An int. The address where the  
                key is supposed to hash too. When an address
                is provided, hashing of the key is skipped.
    """

    # guardians for parameters
    try:
      guardian = KeyAssertion()
      guardian(key)
      if not address:
        address = self.Hash(key)
        guardian = BucketAssertion(1, self.num_buckets) 
    except Exception as e:
      raise(e)

    if DEBUGMODE:
      print("[DEBUG][Delete][Parameters] key: ", key) 
      print("[DEBUG][Delete][Parameters] address: ", address)
      print("[DEBUG][Delete][State] keys:", self.keys)

    # delete data from storage via tombstoning
    if DEBUGMODE:
      print("[DEBUG][Delete][State] key: ", key)
      print("[DEBUG][Delete][State] address: ", address)
    node = self.Search(key, address)
    if node:
      node.key, node.value = "", None
      if DEBUGMODE:
        str_data = str(node.value)
        print("[DEBUG][Delete][Update] node: ", node)
        print("[DEBUG][Delete][Update] node key: ", node.key)
        print("[DEBUG][Delete][Update] node value: ", str_data)
        print("[DEBUG][Delete][Update] node next: ", node.next)

    # delete key from container
    if key in self.keys:
      self.keys.discard(key)
      self.num_keys -= 1
    if DEBUGMODE: 
      print("[DEBUG][Delete][End]: keys", self.keys)
      print("[DEBUG][Delete][End]: num_keys", self.num_keys)


  def Sort(self):
    """
      Returns a list of keys sorted alphabetically.
    """

    # Employ strategy object
    strategy = SortStrategy()
    return strategy(self.keys)

  
  def Grow(self):
    """
      Doubles the size of storage when it's half full.
    """

    if DEBUGMODE: 
      print("[DEBUG][Grow][State]: storage", self.storage)

    # increase size of storage
    extension = self.storage[:1]
    extension[0] = ""
    m, n = 1, self.num_buckets
    while m < n:
      m *= 2
      extension += extension
    self.storage += extension
    if DEBUGMODE: 
      print("[DEBUG][Grow][Update]: storage", self.storage)

    # update trackers
    self.num_buckets *= 2
    self.num_empty_buckets += n
    if DEBUGMODE: 
      print("[DEBUG][Grow][Update]: num_buckets", self.num_buckets)
      print("[DEBUG][Grow][Update]: num_empty_buckets", self.num_empty_buckets)

    # rehash keys
    num_buckets = self.num_buckets
    for key in self.keys:
      old_hash = self.Hash(key, num_buckets // 2)
      if DEBUGMODE:
        print("[DEBUG][Grow][State] key: ", key)
        print("[DEBUG][Grow][State] old address: ", old_hash)
      node = self.Search(key, old_hash)

      # handle old hash being too big during recursive grow calls )
      if not node:
        break
      
      # move data
      data = node.value
      if DEBUGMODE:
        str_data = str(data)
        print("[DEBUG][Grow][Loop] key: ", key)
        print("[DEBUG][Grow][Loop] old address: ", old_hash)
        print("[DEBUG][Grow][Loop] node: ", node)
        print("[DEBUG][Grow][Loop] node key: ", node.key)
        print("[DEBUG][Grow][Loop] node value: ", str_data)
        print("[DEBUG][Grow][Loop] node next: ", node.next)
        
      self.Delete(key, old_hash)

      if DEBUGMODE:
        print("[DEBUG][Grow][State] storage: ", self.storage)

      self.Insert(key, data)

      if DEBUGMODE:
        print("[DEBUG][Grow][End] storage: ", self.storage)
    



class Node(object):
    """
      A high-level implementation of a node for building a linked list.

      Attributes
      ----------          
      key : A str used as the label for the data in the node.

      next : Either another node, or the None type.

      value : Either data, or the None type.

      Disclaimer
      ----------
      The HashMap creates a linked list at each address in storage,
      in order to handle hash collisions.

    """

    def __init__(self, key, data):
      """
        The constuctor of the Node class. 

        Parameters
        ----------
        data : Anything that's not a None type 
        
        key : A str used as the label for the data in the node. 
      """
      # create attributes
      self.key = key
      self.value = data
      self.next = None
      if DEBUGMODE:
        str_data = str(self.value)
        print("[DEBUG][init][Assignment] node: ", self)
        print("[DEBUG][init][Assignment] node key: ", self.key)
        print("[DEBUG][init][Assignment] node value: ", str_data)
        print("[DEBUG][init][Assignment] node next: ", self.next)

    def __repr__(self):
      """
        Provides representation when printed.  
      """
      return f"Node(key={self.key})"


# Assertion Classes ----------------------------------------


class KeyAssertion(object):
  """
    A collection of tests for a hash map key.

    Attributes
    ----------          
    MAXSTRLENGTH : An int. The limit to the length of a key.

    Methods
    -------
    AssertType : Asserts a key is a str type

    AssertLength : Asserts the key is an acceptable length.
  """

  def __init__(self, maxlength=50):
    """
      The constructor of the KeyAssertion class.

      Parameters
      ----------
      maxlength : An int. The limit to the length of a key.
    """
    # initialise constants
    self.MAXLENGTH = maxlength

  def __call__(self, key):
    """
        Allows the use of parentheses to deploy assertions.

        Parameters
        ----------
        key : A key for a HashMap object.
    """
    try:
      self.AssertType(key)
      self.AssertLength(key)
    except Exception as e:
      raise(e)

  def AssertType(self, key):
    """
      Asserts key is a string.
    """
    try:
      assert type(key) == str
    except Exception as e:
      raise(Exception("Input needs to be a string."))

  def AssertLength(self, key):
    """
      Asserts key has correct length.
    """
    try:
      assert len(key) >= 1
      assert len(key) <= self.MAXLENGTH
    except Exception as e:
      raise(Exception("Input too short or too long."))


  
class BucketAssertion(object):
  """
    A collection of tests for a number.

    attributes
    ----------
    SMALLEST : The smallest number in the acceptable range.

    LARGEST : The smallest number above the acceptable range. 

    Methods
    -------
    AssertType : Asserts a num is int type.

    AssertRange : Asserts the num is in the correct range.
  """

  
  def __init__(self, start=0, stop=float("Inf")):
    """
      The constructor of the BucketAssertion class.

      Parameters
      ----------
      start : The smallest number in the acceptable range.

      stop : The smallest number above the acceptable range. 

    """
    # initialise constants
    self.SMALLEST = start
    self.LARGEST = stop


  def __call__(self, num):
    """
      Allows the use of parentheses to deploy assertions.

      Parameters
      ----------
      num : A number.
    """
    try:
      self.AssertType(num)
      self.AssertRange(num)
    except Exception as e:
      raise(e)


  def AssertType(self, num):
    """
      Asserts num is an int.
    """
    try:
      assert type(num) == int
    except Exception as e:
      raise(Exception("Input needs to be an int."))


  def AssertRange(self, num):
    """
      Asserts num is in correct range
    """
    try:
      assert num >= self.SMALLEST
      assert num < self.LARGEST
    except Exception as e:
      raise(Exception("The provided number is too big or too small."))

  

class StorageAssertion(object):
  """
    A collection of tests for a hash map storage object.

    Methods
    -------
    AssertLengthFlexibility : Asserts the storage can be 
                              resized.

    AssertDataMutability : Assert data can be inserted and
                           updated in storage.
  """
    

  def __init__(self):
    """
      The constructor of the StorageAssertion class.
    """
    pass


  def __call__(self, storage):
    """
      Allows the use of parentheses to deploy
      assertions.

      Parameters
      ----------
      storage : A container object that should support 
                indexing using integers, data mutations, 
                slicing, and concatenation with itself.
    """
    try:
      storage = self.AssertLengthFlexibility(storage)
      storage = self.AssertDataMutability(storage)
      return storage
    except Exception as e:
      raise(e)


  def AssertLengthFlexibility(self, storage):
    """
      Asserts storage can be resized using 
      concatenation with itself, and slicing.
    """
    try:
      storage += storage
      storage = storage[:1]
      return storage
    except Exception as e:
      raise(Exception("Object should be slicable and concatenable."))


  def AssertDataMutability(self, storage):
    """
      Asserts data can be inserted and updated
      using index notation.
    """
    try:
      storage[0] = "1"
      storage[0] = ""
      return storage
    except Exception as e:
      raise(Exception("Object should be mutable."))



class KeyContainerAssertion(object):
  """
    A collection of tests for a hash map keys container object.

    Methods
    -------
    AssertMethods : Asserts correct methods exist.

    AssertLookups : Assert lookups behave correctly.

    AssertConversions : Assert container can be converted to list.

    Disclaimer
    ----------
    No tests have been created to test dynamic resizing, as no
    algorithm for dynamic resizing is needed for the keys 
    container in this demo.
  """
    
  def __init__(self):
    """
      The constructor of the KeyContainerAssertion class.
    """
    pass


  def __call__(self, container):
    """
      Allows the use of parentheses to deploy
      assertions.

      Parameters
      ----------
      container : An object that should support 
                  .add(), .discard(), and .difference() 
                  methods, conversion into a list, 
                  lookups using the in keyword, 
                  and dynamic resizing.
    """
    try:
      container = self.AssertMethods(container)
      container = self.AssertLookups(container)
      container = self.AssertConversions(container)
      return container
    except Exception as e:
      raise(e)


  def AssertMethods(self, container):
    """
      Asserts correct methods exist.
    """
    try:
      container.add("1")
      container.difference(container)
      container.discard("1")
      return container
    except Exception as e:
      raise(Exception("Object should have .add(), .difference() and .discard() methods."))


  def AssertLookups(self, container):
    """
      Asserts lookups behave as expected.
    """
    try:
      container.add("1")
      assert "1" in container
      difference = container.difference(container)
      assert "1" not in difference
      container.discard("1")
      assert "1" not in container
      return container
    except Exception as e:
      raise(Exception("Object should accept lookups with the in keyword."))


  def AssertConversions(self, container):
    """
      Asserts container can be converted into list.
    """
    try:
      container.add("1")
      assert [key for key in container]
      container.discard("1")
      return container
    except Exception as e:
      raise(Exception("Object should be convertable into a list."))


# Strategy Classes -----------------------------------------


class SortStrategy(object):
  """
    A collection of sorting algorithms. 

    Attributes
    ----------
    THRESHOLDS : a dict that maps containers to algorithms 
                 by their length.

    Methods
    -------
    InsertionSort : The insertion sorting algorithm

    MergeSort : A hybrid merge sorting algorithm
  """

  def __init__(self):
    """
      The constructor of the SortStrategy class.
    """
    # initialise constants
    self.THRESHOLDS = {
      1 : None,
      2 : self.InsertionSort,
      43 : self.MergeSort
    }


  def __call__(self, container):
    """
      Allows the use of parentheses to employ the 
      strategy.

      Parameters
      ----------
      container : A collection that can be iterated
                  over.
    """

    # convert collection to list
    if type(container) != list:
      items = [item for item in container]
    else:
      items = container
    if DEBUGMODE:
      print("[DEBUG][Sort][Parameter] items: ", items)
    
    # get strategy
    length, strategy = len(items), None
    for key in self.THRESHOLDS.keys():
      if length >= key:
        strategy = self.THRESHOLDS[key]
      else:
        break

    if DEBUGMODE:
      print("[DEBUG][Sort][Assignment] strategy: ", strategy.__name__ if strategy else "None")

    
    # employ strategy
    if strategy:
      return strategy(items)
    else:
      return items


  def InsertionSort(self, container):
    """
      An implementation of the insertion sort algorithm,
      that returns a sorted list.

      Parameters
      ----------
      container : A list to be sorted.
    """

    # maintain sorting invariant for container[:i]
    length = len(container)
    for i in range(1,length):
      # insert by swapping
      if DEBUGMODE:
        print("[DEBUG][Sort][Loop] container: ", container) 
        print("[DEBUG][Sort][Loop] index: ", i)  

      for j in range(i, 0, -1):
        if container[j] < container[j-1]:
          container[j], container[j-1] = container[j-1], container[j]
        else:
          continue

      if DEBUGMODE:
        print("[DEBUG][Sort][Loop] container: ", container) 

    if DEBUGMODE:
      print("[DEBUG][Sort][Output] container: ", container)   
    return container

  
  def MergeSort(self, container):
    """
      An implementation of the merge sort algorithm,
      that returns a sorted list. InsertionSort is
      used for small divisions.

      Parameters
      ----------
      container : A list to be sorted.
    """

    # divide
    length = len(container)
    mid = length // 2
    left, right = container[:mid], container[mid:]
    if DEBUGMODE:
      print("[DEBUG][Sort][Recursion] left: ", left) 
      print("[DEBUG][Sort][Recursion] right: ", right)  

    # sort each division
    left = self(container[:mid])
    right = self(container[mid:])

    # merge
    complete = []
    while left and right:
      if DEBUGMODE:
        print("[DEBUG][Sort][Loop] left: ", left) 
        print("[DEBUG][Sort][Loop] right: ", right)

      if left[0] < right[0]:
        complete.append(left.pop(0))
      else:
        complete.append(right.pop(0))

      if DEBUGMODE:
        print("[DEBUG][Sort][Loop] left: ", left) 
        print("[DEBUG][Sort][Loop] right: ", right)
        print("[DEBUG][Sort][Loop] container: ", complete)

    if left:
      complete.extend(left)
    if right:
      complete.extend(right)
    if DEBUGMODE:
      print("[DEBUG][Sort][Output] container: ", complete)

    return complete


# Database -------------------------------------------------

# Database Management Classes ------------------------------


class EntityDBM(object):
  """
    A  non-relational database management class to provide
    an API for interfaces. The database architecture draws
    upon an entity-field data model, and provides CRUD operations.  

    Attributes
    ----------
    db : A HashMap data structure for organising data in memory.

    name: A name for the database.

    Methods
    -------
    AddEntity : Adds a new entity to the HashMap.

    AddData : Adds data to an entity field.

    ViewEntities : Returns all entities sorted in alphabetical order.

    ViewEntity : Returns all information about an an entity.

    DeleteEntity : Deletes data baout an entity.

    SortTable : Sorts a table by a field.

    FilterTable : Filters a table by a field.

    ClearAll : Deletes all data.
  """
  
  def __init__(self, db_name):
    """
      The constructor of the EntityDBMS class.

      Parameters
      ----------
      db_name : A str that provides a name for the database.
    """

    # Guardians for parameters
    try:
      guardian = KeyAssertion()
      guardian(db_name)
    except Exception as e:
      raise(e)

    # initialise attributes
    self.name = db_name
    self.db = HashMap(db_name)

  
  def __contains__(self, key):
    """
      Allows the use of the 'in' keyword.

      Parameters
      ----------
      key : A str. A label associated with data.
    """

    # return a bool depending on whether key is being tracked.
    return key in self.db


  def AddEntity(self, name):
    """
      Adds an entity to the database.

      Parameters
      ----------
      name : A str that provides a name for the entity.

    """

    # Insert entity with name into hashmap
    key, data, nested_keys = name, name, ["name"]
    if DEBUGMODE:
      print("[DEBUG][AddEntity][Assignment] entity: ", name)
      print("[DEBUG][AddEntity][Assignment] field: ", nested_keys[0])
      print("[DEBUG][AddEntity][Assignment] data: ", name)

    if name not in self.db:
      self.db.Insert(data, key, nested_keys)
      if DEBUGMODE:
        print("[DEBUG][AddEntity][End] name: ", name)
      return True
    else:
      return False


  def AddData(self, name, field, data):
    """
      Adds data about an entity.

      Parameters
      ----------
      name : A str that provides a name for the entity.

      field : A str that provides a key for the data.

      data : Anything.

    """
    # Insert data about item into hashmap
    key, data, nested_keys = name, data, [field]
    if DEBUGMODE:
      print("[DEBUG][AddData][Assignment] entity: ", key)
      print("[DEBUG][AddData][Assignment] field:", nested_keys[0])
      print("[DEBUG][AddData][Assignment] data: ", data)

    if name in self.db:
      self.db.Insert(key, data, nested_keys)
      if DEBUGMODE:
        print("[DEBUG][AddData][End] name: ", name)
      return True
    else:
      return False

  
  def ViewEntities(self, extra_fields=False):
    """
      Returns a table of all entities and selected fields.

      Parameters
      ----------
      extra_fields : A list of entities fields to include in the table.
    """

    # get fields
    fields = ["name"]
    if extra_fields:
      fields.extend(extra_fields)
    if DEBUGMODE:
      print("[DEBUG][ViewEntities][Parameter] fields: ", fields)

    # create table
    keys = self.db.keys
    entities = [self.db[x] for x in keys if x != "name"]
    table = [[entity[field] if field in entity else f"{field} not specified" for field in fields] for entity in entities]
    if DEBUGMODE:
      str_entities, str_table = str(entities), str(table)
      print("[DEBUG][ViewEntities][Assignment] entities: ", str_entities)
      print("[DEBUG][ViewEntities][Output] table: ", str_table)
      
    return table


  def ViewEntity(self, name):
    """
      Returns a table of all information about an entity.

      Parameters
      ----------
      name : A str. The name of the entity.
    """ 
    if DEBUGMODE:
      print("[DEBUG][ViewEntity][Parameter] name: ", name)

    # create table
    rows = []
    data = self.db[name]
    if data:
      for key in data.keys:
        rows.append([key, data[key]])
    if DEBUGMODE:
      str_rows = str(rows)
      print("[DEBUG][ViewEntity][Output] table: ", str_rows)

    return rows
  

  def DeleteEntity(self, name):
    """
      Deletes all data about a specified entity.

      Parameters
      ----------
      name : A str. The name of the entity.
    """

    if DEBUGMODE:
      print("[DEBUG][DeleteEntity][Parameter] name: ", name)

    # delete entity
    if name in self.db:
      self.db.Delete(name)
      return True
    else:
      return False


  def SortTable(self, table, extra_fields, sort_key, sort_ascending):
    """
      Sorts the rows in a table.

      Parameters
      ----------
      table : A table of records to sort.

      extra_fields : Table headers.

      sort_key : A field to sort by.

      sort_ascending : A bool indicating the direction to sort.
    """

    # get sort parameters
    fields = ["name"] + extra_fields
    fields_index = fields.index(sort_key)
    if DEBUGMODE:
      print("[DEBUG][SortTable][Parameter] table: ", table)
      print("[DEBUG][SortTable][Parameter] fields:", fields)
      print("[DEBUG][SortTable][Parameter] sort_key: ", sort_key)
      print("[DEBUG][SortTable][Parameter] sort_ascending: ", sort_ascending)

    # sort subtable
    subtable = [(row[fields_index], row[0]) for row in table]
    strategy = SortStrategy()
    subtable = strategy(subtable)

    # reverse subtable if required
    if not sort_ascending:
      subtable = subtable[::-1]
    if DEBUGMODE:
      str_subtable = str(table)
      print("[DEBUG][SortTable][Assignment] subtable: ", str_subtable)

    # create table
    entities = [self.db[x[1]] for x in subtable]
    table = [[entity[field] if field in entity else f"{field} not specified" for field in fields] for entity in entities]
    if DEBUGMODE:
      str_entities, str_table = str(entities), str(table)
      print("[DEBUG][SortTable][Assignment] entities: ", str_entities)
      print("[DEBUG][SortTable][Output] table: ", str_table)
    
    return table

  
  def FilterTable(self, table, extra_fields, filter_key, value):
    """
      Filters the rows of the table by the specified field,
      matching only rows with the specified field value.

      Parameters
      ----------
      table : A table of records to filter.

      extra_fields : Table headers.

      filter_key : A field to filter by.

      value : A value to assert the field should be
    """

    # get filter parameters
    fields = ["name"] + extra_fields
    num_fields = len(fields)
    for i in range(num_fields):
      if fields[i] == filter_key:
        fields_index = i
        break
    else:
      return []

    if DEBUGMODE:
      print("[DEBUG][FilterTable][Parameter] table: ", table)
      print("[DEBUG][FilterTable][Parameter] fields:", fields)
      print("[DEBUG][FilterTable][Parameter] filter_key:", filter_key)
      print("[DEBUG][FilterTable][Parameter] value: ", value)
    
    # filter table
    filtered_table = []
    for row in table:
      if DEBUGMODE:
        print("[DEBUG][FilterTable][Loop] row: ", row)
      if row[fields_index] == value:
        filtered_table.append(row)
    if DEBUGMODE:
      print("[DEBUG][FilterTable][Output] filtered_table: ", filtered_table)
    return filtered_table

  
  def AddRandomItems(self, amount):
    """
      Adds an amount of random items to the database.

      Paramaters
      ----------
      amount : The amount of items to add.

      Disclaimer
      ----------
      The amount of inserted items may be lower than 
      expected due to the random generator picking the
      same item more than once, which doesn't result in the item
      being inserted again.
    """

    # Get items
    factory = Food()
    for _ in range(amount):
      item = factory.RandomItem()
      if DEBUGMODE:
        print("[DEBUG][AddRandomItems][Loop] item: ", item)
      self.AddEntity(item)
      
      # Add details
      colour = factory.RandomColour()
      if DEBUGMODE:
        print("[DEBUG][AddRandomItems][Loop] colour: ", colour)
      self.AddData(item, "colour", colour)
      expiry_date = factory.RandomExpiryDate()
      if DEBUGMODE:
        print("[DEBUG][AddRandomItems][Loop] expiry date: ", expiry_date)
      self.AddData(item, "expiry date", factory.RandomExpiryDate())
    


  def ClearAll(self):
    """
      Deletes all data in the database.
    """
    self.db = HashMap(self.name)
    if DEBUGMODE:
      str_db = str(self.db)
      print("[DEBUG][ClearAll][Update] database: ", str_db)


# Interfaces -----------------------------------------------


class CLI(object):
  """
    A command line interface helper class for Dionysus.

    Disclaimer
    ----------
    The list of attributes and methods haven't been included here
    due to the large quanity of them.
  """

  def __init__(self, wait=0.3):
    """
      The constructor of the CLI class.

      Parameters
      ----------

      wait : an amount of time to wait before new messages
    """

    # Initialise constants
    self.ADDEDDB = "Food inventory has been created successfully!"
    self.ADDEDENTITY = "Item has been added to the inventory successfully!"
    self.ADDEDDATA = "Item has been given new details successfully!"
    self.ASKSELECTION = "What would you like to do?"
    self.CONFIRMATION = "You entered the word: "
    self.db = None
    self.GOODBYE = "Goodybe. Thank you for using Dionysus App."
    self.EXTRAINFO = "Would you like to add more details to the item? (y/n)"
    self.FIELD = "What type of details are you providing? (amount, colour, expiriy date, etc.): "
    self.MORE = "Please provide some information about it."
    self.NEWDB = "Please choose a name for your food inventory: "
    self.NEWITEM = "Please give the name of the item: "
    self.OK = "Is that OK? (y/n): "
    self.OPTIONS = [
      "Add a new item",
      "Remove an item",
      "Provide new details about an item",
      "View all details about an item",
      "View a list of all items",
      "View a filtered list of items",
      "Remove all items",
      "Turn debug mode on or off",
      "Add loads of random items",
      "Exit"
    ]
    self.SELECTION = "You chose the option: "
    self.TRYAGAIN = "Would you like to try again? (y/n): "
    self.WAIT = wait
    self.WARNING = "Error Received: \n"
    self.WELCOME = "Welcome to Dionysus App."


  def __call__(self, selection):
    """
      Allows the use of parentheses to handle a selection.

      Parameters
      ----------
      selection : An int that represents a possible interaction
                  with the database.
    """
    
    # guardians for parameters
    try:
      command = self.OPTIONS[selection - 1]
    except Exception as e:
      raise(e)

    # handle command
    if command == "Add a new item":
      # get item to add
      self.Print(self.MORE)
      name = self.EntityName()
      if name:
        if self.db.AddEntity(name):
          self.Print(self.ADDEDENTITY)
          # get more details from user to add to entity
          while self.YesNo(self.EXTRAINFO):
            data = self.Details()
            if data:
              self.db.AddData(name, data[0], data[1])
              self.Print(self.ADDEDDATA)
        else:
          self.Print("Item was already being tracked!")
    elif command == "Provide new details about an item":
      # get details to add to item
      name = self.EntityName()
      if name:
        data = self.Details()
        while data:
          # add item first if required
          if name not in self.db:
            self.db.AddEntity(name)
            self.Print(self.ADDEDENTITY)
          self.db.AddData(name, data[0], data[1])
          self.Print(self.ADDEDDATA)
          # get more details from user to add to entity
          if not self.YesNo(self.EXTRAINFO):
            break
          else:
            data = self.Details()
    elif command == "View a list of all items":
      # get the fields to view
      extra_fields = self.Fields()
      items = self.db.ViewEntities(extra_fields)
      # sort table
      sort_key, sort_ascending = self.SortKey(extra_fields)
      items = self.db.SortTable(items, extra_fields, sort_key, sort_ascending)
      while items:
        # show table
        num_items = len(items)
        for i in range(num_items):
          print(f"{i+1}. {items[i]}")
        input("Press enter when you are ready to move on.")
        # allow alternative sorting
        if self.YesNo("Would you like to sort the table again? (y/n)"):
          sort_key, sort_ascending = self.SortKey(extra_fields)
          items = self.db.SortTable(items, extra_fields, sort_key, sort_ascending)
          continue
        # allow filtering
        if self.YesNo("Would you like to filter the table? (y/n)"):
          data = self.Details()
          if data:
            items = self.db.FilterTable(items, extra_fields, data[0], data[1])
        else:
          break
      else:
        self.Print("There's no items to view.")
    elif command == "View a filtered list of items":
      # get the fields to view
      extra_fields = self.Fields()
      items = self.db.ViewEntities(extra_fields)
      # filter table
      self.Print("Details must be provided in order to filter the table.")
      data = self.Details()
      if data:
          items = self.db.FilterTable(items, extra_fields, data[0], data[1])
      else:
        self.Print("No filter was applied.")
      while items:
        # show table
        num_items = len(items)
        for i in range(num_items):
          print(f"{i+1}. {items[i]}")
        input("Press enter when you are ready to move on.")
        # allow alternative filtering
        if self.YesNo("Would you like to filter the table again? (y/n)"):
          data = self.Details()
          if data:
            items = self.db.FilterTable(items, extra_fields, data[0], data[1])
            continue
          else:
            self.Print("No filter was applied.")
        # allow alternative sorting
        if self.YesNo("Would you like to sort the table? (y/n)"):
          sort_key, sort_ascending = self.SortKey(extra_fields)
          items = self.db.SortTable(items, extra_fields, sort_key, sort_ascending)
        else:
          break
      else:
        self.Print("There's no items to view.")
    elif command == "View all details about an item":
      # view an entity
      name = self.EntityName()
      if name:
        table = self.db.ViewEntity(name)
        if table:
          for row in table:
            print(f"[DETAIL] {row[0]}: {row[1]}")
          input("Press enter when you are ready to move on.")
        else:
            self.Print("There's no information to view.")
    elif command == "Exit":
      # end application
      return False
    elif command == "Turn debug mode on or off":
      # turn debug mode on or off
      global DEBUGMODE
      DEBUGMODE = not DEBUGMODE
      self.Print(f"Debug Mode switched {'on' if DEBUGMODE else 'off'}")
    elif command == "Remove an item":
      # delete an entity
      name = self.EntityName()
      if name:
        if self.db.DeleteEntity(name): 
          self.Print(f"Item has been deleted from the inventory successfully!")
        else:
          self.Print(f"The item didn't exist in the the inventory!")
    elif command == "Remove all items":
      # delete all data in the database 
      self.db.ClearAll()
      self.Print(f"All data has been deleted.")
    elif command == "Add loads of random items":
      while True:
        response = input("Please enter how many random items you would like to add (1-1000): ")
        try:
          response = int(response)
          guardian = BucketAssertion()
          guardian(response)
          self.db.AddRandomItems(response)
          self.Print(f"{response} items have been added to the inventory successfully!")
          break
        except Exception as e:
          self.Print(self.WARNING + str(e))
          if self.TryAgain():
            continue
          else:
            break 
    else:
      # restart procedure
      self.Print(f"Didn't understand the command: {command}")
    return True


  def Print(self, message):
    """
      Prints a message and adds a time delay for better UX.

      Parameters
      ----------
      message: A message displayed to the user.
    """
    print(message)
    sleep(self.WAIT)

  
  def Keyword(self, message, maxlength=20):
    """
      Asks for a keyword.

      Parameters
      ----------
      maxlength : An int representing the maximum
                  length for the input. 

      message : A message displayed to the user.
    """

    # get input
    keyword = input(message)
    sleep(self.WAIT)

    # guardians for input
    try:
      guardian = KeyAssertion(maxlength)
      guardian(keyword)
      self.Print(self.CONFIRMATION + keyword)
    except Exception as e:
      self.Print(self.WARNING + str(e))
      if self.TryAgain():
        return self.Keyword(message)
      else:
        return None

    # oppurtunity for user correction
    if self.Continue():
      return keyword
    elif self.TryAgain():
      return self.Keyword(message)
    else:
      return None

  
  def YesNo(self, message):
    """
      Asks user for yes or no answer.

      Parameters
      ----------
      message : A message displayed to the user.
    """

    # get input
    response = input(message)
    sleep(self.WAIT)

    # decipher input
    return response[0].lower() == "y" if response else True

  
  def AcknowledgeDB(self, db):
    """
      Pairs the db with this interface.

      Parameters
      ----------
      db : An EntityDBM object for interacting with a database.

    """
    self.db = db
    self.Print(self.ADDEDDB)


  def Welcome(self):
    """
      Gives a welcome message.
    """
    self.Print(self.WELCOME)


  def Goodbye(self):
    """
      Gives a goodbye message.
    """
    self.Print(self.GOODBYE)


  def DBName(self):
    """
      Gets a database name.
    """
    return self.Keyword(self.NEWDB)


  def EntityName(self):
    """
      Gets an entity name.
    """
    return self.Keyword(self.NEWITEM)

  
  def TryAgain(self):
    """
      Asks user to try again.
    """
    return self.YesNo(self.TRYAGAIN)


  def Continue(self):
    """
      Asks user to continue.
    """
    return self.YesNo(self.OK)


  def Options(self, options="default", ask="default"):
    """
      Provide a set of options for the user to choose from.

      Parameters
      ----------
      options : An array of options for the user to select from.
    """

    # state options
    if options == "default":
      options = self.OPTIONS
    if ask == "default":
      ask = self.ASKSELECTION
    self.Print(ask)
    for i, option in enumerate(options):
      print(f"{i+1}. {option}")

    # get selection
    num_options = len(options)
    selection = input(f"Selection (1-{num_options}): ")
    sleep(self.WAIT)

    # guardians for input
    try:
      selection = int(selection)
      guardian = BucketAssertion(1, num_options+1)
      guardian(selection)
      self.Print(self.SELECTION + f"'{options[selection - 1]}'")
    except Exception as e:
      self.Print(self.WARNING + str(e))
      if self.TryAgain():
        return self.Options()
      else:
        return None 

    # oppurtunity for user correction
    if self.Continue():
      return selection
    elif self.TryAgain():
      return self.Options()
    else:
      return None
  

  def Details(self):
    """
      Asks user for some additional details about an item.
    """
    # Get details
    field = self.Keyword(self.FIELD)
    if field:
      data = self.Keyword(f"What is the {field}?")
      if data:
        return field, data
      else:
        return None


  def Fields(self):
    """
      Asks user for some additional fields to view.
    """
    # gets extra field names from user
    extra_fields = ["name"]
    while True:
      self.Print(f"Details to be included are: {extra_fields}")
      if self.YesNo("Would you like to include anymore details? (y/n): "):
        field = self.Keyword("Please enter another type of detail to include (amount, colour, expiriy date, etc.): ")
        if field:
          extra_fields.append(field)
      else:
        break

    return extra_fields[1:] if len(extra_fields) > 1 else []


  def SortKey(self, extra_fields):
    """
      Asks user to select a field to sort by.
    """
    # gets options
    fields = ["name"] + extra_fields
    if DEBUGMODE:
      print("[DEBUG][SortKey][Assignment] fields: ", fields)

    # gets field and direction
    selection = self.Options(fields, "Which field would you like to sort the list by?")
    if selection:
      selection -= 1
    else:
      selection = 0
    if DEBUGMODE:
      print("[DEBUG][SortKey][Assignment] Selection: ", selection)

    sort_ascending = self.YesNo(f"Would you like to sort by '{fields[selection]}' in ascending order? (y/n)")

    return fields[selection], sort_ascending


# Test Data ------------------------------------------------

class Food(object):
  """
    A class to provide test data.

    Methods
    -------
    RandomItem : Provides a procedurally generated item.

    RandomColour : Provides a random colour

    RandomExpiryDate : Provides a random expiry date
  """

  def __init__(self):
    """
      The constructor of the Food class.
    """
    
    # initialise constants
    self.FOODA = [
      "artificial", "baby", "bagged", "baked", "battered", "blended", "boiled", "canned", "creamy", "crispy", "condensed", 
      "darkend", "distilled", "drained", "dried", "flattened", "fried", "frozen", "full-fat", "garnished", "grated", "large", "loaded", 
      "magic", "marinated", "mashed", "mature", "melted", "microwaved", "organic", "packaged", "pale", "pickled", "plated",
      "processed", "powdered", "raw", "roasted", "salted", "seasoned", "small", "soft", "spicy", "spotted", 
      "squashed", "sour", "sweet", "sugar-coated", "tangy", "tinned", "tough", "unpackaged",
      "vegan", "whipped"
    ]

    self.FOODB = [
      "apple", "almond", "bacon", "banana", "bean", "beef", "blackcurrant", "brocolli", "caramel", "carrot", "cauliflower", "caviar", 
      "coffee", "chicken", "chilli", "chocolate", 
      "cinnamon", "crab", "duck", "egg", "garlic", "grape", "hazlenut", "honey", 
      "kiwi", "lemon", "lobster", "marmite", "marshmallow", "meatball", "mushroom", 
      "mint", "olive", "onion", "orange", "parsley",  "pear", "peanut", "pepper", "pineapple", "pork", "potato", "prawn", "pumpkin",
      "radish", "raisin", "raspberry", "rice", "salmon", "sausage", "strawberry", "sweetcorn", "tomato", "tuna", "tofu", 
      "vanilla", "walnut", "wasabi", "yoghurt" 
    ]

    self.FOODC = [
      "baguette", "bread", "burger", "butter", "cake", "chips", "crisps", "croissant", "cookies",
      "curry", "desert", "fingers", "jam", "juice", 
      "kebab", "lasagne", "mayonaise", "milk", "mix", "mustard", "noodles", "oil", "omlette", "pastry", "pie", "pudding", 
      "quiche", "rings", "roll", "rum", "salad", "salsa", "sandwich", "sauce", "skewers",
      "smoothie", "soda", "soup", "spaghetti", "spread", "stew", "stirfry", 
      "taco", "tart", "wine", "wrap", "vodka"
    ]

    self.COLOURS = [
      "red", "orange", "brown", "green", "yellow",
       "white", "pink", "blue", "purple",
    ]

    self.EXPIRY = [
      "today", "tomorrow", "this week", "next week", "this month", 
      "next month", "this year", "next year", "never"
    ]

  
  def RandomItem(self):
    """
      Returns a random item.
    """

    # decide how to combine words
    combo_rng = choice([1,2,3,4,5,6])

    # create item
    item = choice(self.FOODB)
    main = side = item
    if DEBUGMODE:
      print("[DEBUG][RandomItem][Assignment] combo_rng", combo_rng)
      print("[DEBUG][RandomItem][Assignment] item", item)
    if combo_rng % 3 == 0:
      item = choice(self.FOODA) + " " + item
      if DEBUGMODE:
        print("[DEBUG][RandomItem][Update] item: ", item)
    if combo_rng < 4:
      while side == main:
        side = choice(self.FOODB)
      item += " and " + side
      if DEBUGMODE:
        print("[DEBUG][RandomItem][Update] item: ", item)
    if combo_rng % 2 == 0:
      item += " " + choice(self.FOODC)
      if DEBUGMODE:
        print("[DEBUG][RandomItem][Update] item: ", item)
    if DEBUGMODE:
      print("[DEBUG][RandomItem][Output] item: ", item)

    return item
  

  def RandomColour(self):
    """
      Returns a random colour
    """
    return choice(self.COLOURS)


  def RandomExpiryDate(self):
    """
      Returns a random expiry date
    """
    return choice(self.EXPIRY)


# Script ---------------------------------------------------


# Determine whether file is being run as a script or a module
if __name__ == "__main__":
  # initialise command line interface
  cli = CLI(1)

  # initialise database
  cli.Welcome()
  name = cli.DBName()
  if name:
    food_inv = EntityDBM(name)
    cli.AcknowledgeDB(food_inv)

    # handle interactions
    selection = cli.Options()
    while selection:
      if not cli(selection):
        break
      else:
        selection = cli.Options()
  # end app
  cli.Goodbye()
