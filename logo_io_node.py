#!/usr/bin/env python

class IO_Node:
    def __init__(self, _id, _logo, _readAddress, _readBit, _writeOnAddress, _writeOnBit, _writeOffAddress, _writeOffBit, _writeAddress, _writeBit, _rwLenght, _invertResult, _text):
        self.n_id              = _id
        self.n_logo            = _logo
        self.n_readAddress     = _readAddress
        self.n_readBit         = _readBit
        self.n_writeOnAddress  = _writeOnAddress
        self.n_writeOnBit      = _writeOnBit
        self.n_writeOffAddress = _writeOffAddress
        self.n_writeOffBit     = _writeOffBit
        self.n_writeAddress    = _writeAddress
        self.n_writeBit        = _writeBit
        self.n_rwLenght        = _rwLenght
        self.n_invertResult    = _invertResult
        self.n_text            = _text


class IO_Page:
    def __init__(self, _id, _nodeArray, _text):
        self.p_id = _id
        self.p_nodeArray = _nodeArray
        self.p_text = _text


                        #      ID
                        #      |      Logo
                        #      |      |     Read Address
                        #      |      |     |  Read Bit
                        #      |      |     |  |    Write On Address
                        #      |      |     |  |    |  Write On Bit
                        #      |      |     |  |    |  |    Write Off Address
                        #      |      |     |  |    |  |    |  Write Off Bit
                        #      |      |     |  |    |  |    |  |    Write Address
                        #      |      |     |  |    |  |    |  |    |  Write Bit
class IO_Array:         #      |      |     |  |    |  |    |  |    |  |   R/W Lenght
    def __init__(self): #      |      |     |  |    |  |    |  |    |  |   |  Invert Result
        self.nodes = [ IO_Node(0,     0,    0, 0,   0, 0,   0, 0,   0, 0,  0, 0, "Dumy"),

                       IO_Node(1,     0, 1064, 0,   0, 0,   0, 0,   1, 0,  1, 0, "Example 1"),
                       IO_Node(2,     0, 1072, 0,   0, 0,   0, 0,   4, 0,  8, 0, "Example 2"),
                       IO_Node(3,     0, 1074, 0,   0, 0,   0, 0,   5, 0, 16, 0, "Example 3"),
                       IO_Node(4,     0, 1076, 0,   0, 0,   0, 0,   6, 0, 32, 0, "Example 4"),

                       IO_Node(5,     1,  942, 0, 100, 0, 200, 0,   1, 4,  1, 0, "Example 5"),
                       IO_Node(6,     1,  942, 1, 100, 1, 200, 1,   1, 5,  1, 0, "Example 6"),
                       IO_Node(7,     1,  942, 2, 100, 2, 200, 2,   2, 3,  1, 1, "Example 7"),
                       IO_Node(8,     1,  942, 3, 100, 3, 200, 3,   2, 4,  1, 1, "Example 8"),

                       IO_Node(9,     0,   92, 0,   0, 0,   0, 0,  90, 0, 16, 0, "Example 9"),
                       IO_Node(10,    0,   94, 0,   0, 0,   0, 0,   0, 0, 16, 0, "Example 10"),

                       IO_Node(11,  255,    0, 0,   0, 0,   0, 0,   3, 0,  1, 0, "Example 11"),
                       IO_Node(12,  255,    0, 0,   0, 0,   0, 0,   3, 1,  1, 0, "Example 12"),
                      ]

        self.pages = [ IO_Page(0, [0],          "Requests for html page 0"),
                       IO_Page(1, [1, 2, 3, 4], "Requests for html page 1"),
                       IO_Page(2, [5, 6, 7, 8], "Requests for html page 2"),
                       IO_Page(3, [9, 10],      "Requests for html page 3"),
                     ]


    def returnNodeWitheID(self, _id):
        for node in self.nodes:
            if node.n_id == _id:
                return node


    def returnPageWitheID(self, _id):
        for page in self.pages:
            if page.p_id == _id:
                return page


# Logo 0BA7
#        Input  24: 923 (Bit)
# Analog Input   8: 926 (Word)
#        Output 16: 942 (Bit)
# Analog Output  2: 944 (Word)
#        Merker 27: 948 (Bit)
# Analog Merker 16: 952 (Word)

# Logo 0BA8 / 8.SF4
#        Input  24: 1024 (Bit)
# Analog Input   8: 1032 (Word)
#        Output 20: 1064 (Bit)
# Analog Output  8: 1072 (Word)
#        Merker 64: 1104 (Bit)
# Analog Merker 64: 1118 (Word)
