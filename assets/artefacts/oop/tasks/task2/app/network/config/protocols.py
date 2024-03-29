'''Designates values for protocols'''

class Basic(object):
    '''
    A container for information about the Basic protocol.

    Headers should include:
        'op' : operation id (for request-responding)
        'address' : the senders id
        'this' : the package sequence number (for package streams)
        'last' : the final package sequence number
    Each value must be an int from 0 to 255.
    '''
    HEAD_SIZE = 32
    HEAD_SEGMENT_SIZE = 8
    BODY_SIZE = 32
    TAGS = ('op', 'address', 'this', 'last')
    OP = {
        "request" : 1,
        "response" : 2
    }
