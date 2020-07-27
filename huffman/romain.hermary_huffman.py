from algopy import bintree
from algopy import heap

################################################################################
## COMPRESSION

def buildfrequencylist(dataIN):
    """
    Builds a tuple list of the character frequencies in the input.
    """
    ListeTuple = []
    AsciiCount = 0
    while AsciiCount < 256:
        i = 0
        LongueurSTR = len(dataIN)
        Character = chr(AsciiCount)
        CharCount = 0
        while i < LongueurSTR:
            if dataIN[i] == Character:
                CharCount += 1
            i += 1
        if CharCount != 0:
            ListeTuple.append((CharCount, Character))
        AsciiCount += 1
    return ListeTuple
    pass


def buildHuffmantree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
    if len(inputList) == 0:
        return bintree.BinTree(None, None, None)

    OccListe = [] #(Occur, Character)
    while len(inputList) > 0:
        maximum = inputList[0][0]
        place = 0
        for i in range(1, len(inputList)):
            if inputList[i][0] >= maximum:
                maximum = inputList[i][0]
                place = i
        OccListe.append((inputList[place][0], bintree.BinTree(inputList[place][1], None, None)))
        inputList.pop(place)

    while len(OccListe) > 1:
        RightChild = OccListe.pop()
        LeftChild = OccListe.pop()
        KeyFirst = RightChild[0] + LeftChild[0]
        FirstBintree = bintree.BinTree(None, LeftChild[1], RightChild[1])
        i = 0
        longeurListe = len(OccListe)
        NewOccList = []
        while i < longeurListe and KeyFirst < OccListe[i][0]:
            NewOccList.append(OccListe[i])
            i += 1
        NewOccList.append((KeyFirst, FirstBintree))
        while i < longeurListe:
            NewOccList.append(OccListe[i])
            i += 1
        OccListe = NewOccList
    return OccListe[0][1]
    pass

# Fonction récursive qui renvoie une liste de couples
# (Caractère, correspondance binaire suivant l'huffmanTree)
# ajoute "0" au string quand la récursion va à gauche, "1" si elle part à droite
# arrivé en bout de récursion, la fonction ajoute le couple correspondant à la liste
def _buildCorrespTable(T, coor, L):
    if T.left is None:
        L.append((T.key, coor))
    else:
        _buildCorrespTable(T.left, coor + "0", L)
        _buildCorrespTable(T.right, coor + "1", L)
    return L


def encodedata(huffmanTree, dataIN):
    """
    Encodes the input string to its binary string representation.
    """
    L = []
    CorresTable = _buildCorrespTable(huffmanTree, "", L)
    res = ""
    for i in range(len(dataIN)):
        j = 0
        while dataIN[i] != CorresTable[j][0]:
            j += 1
        res += CorresTable[j][1]
    return res
    pass

# Convertit un int en octet, sachant que l'int est un code ascii donc ne peut
# pas dépasser 255 et le résultat s'écrira donc sur un maximum de 8 bits.
# Elle renvoie, dans tous les cas, un octet.

def _intToByte(A):
    ToSubstract = 128
    res = ""
    while A != 0 or len(res) < 8:
        if ToSubstract != 0 and A >= ToSubstract:
            A -= ToSubstract
            res += "1"
            ToSubstract = ToSubstract // 2
        else:
            res += "0"
            ToSubstract = ToSubstract // 2
    return res

# Même fonction dans le sens inverse
# Sauf que l'entrée n'est pas forcément un octet
def _byteToInt(A):
    index = len(A) - 1
    multi = 1
    res = 0
    while index >= 0:
        res += int(A[index]) * multi
        multi = multi * 2
        index -= 1
    return res


# Fonction récursive qui prend un huffmanTree et un string en paramètres
# Elle suit les règles de l'énoncé : quand on va à gauche dans l'arbre on ajoute "0",
# quand on arrive sur une feuille elle transforme le caractère en code ASCII (binaire sur un octet)
# précédé d'un "1" et l'ajoute au résultat
def _encodetree(T, res):
    if T.left is None:
        res += "1" + _intToByte(ord(T.key))
        return res
    else:
        res += "0"
        res = _encodetree(T.left, res)
        res = _encodetree(T.right, res)
    return res



def encodetree(huffmanTree):
    """
    Encodes a huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result
    """
    result = _encodetree(huffmanTree, "")
    return result
    pass


def tobinary(dataIN):
    """
    Compresses a string containing binary code to its real binary value.
    """
    i = 0
    longeurString = len(dataIN)
    res = ""
    var = 0
    while i < longeurString:
        j = 0
        _res = ""
        while j < 8 and i < longeurString:
            _res += dataIN[i]
            i += 1
            j += 1
        if j == 8:
            res += chr(_byteToInt(_res))
        else:
            res += chr(_byteToInt(_res))
            i += 1
            var = 8 - j 
    return (res, var)
    pass


def compress(dataIn):
    """
    The main function that makes the whole compression process.
    """
    Freq = buildfrequencylist(dataIn)
    HuffmanTree = buildHuffmantree(Freq)
    EncodedTree = encodetree(HuffmanTree)
    EncodedData = encodedata(HuffmanTree, dataIn)
    var1 = tobinary(EncodedData)
    var2 = tobinary(EncodedTree)
    return (var1, var2)
    pass

################################################################################
## DECOMPRESSION

# Fonction récursive qui renvoie un couple (obj, bool)
# le bool est vrai si la clef renvoyée est celle d'une feuille faux sinon
# l'objet renvoyé est la clef du noeud que l'adresse Coor indique dans l'huffmanTree T
def _decodedata(T, index, Coor):
    if index >= len(Coor):
        return (T.key, T.left is None)
    else:
        if Coor[index] == '0':
            res = _decodedata(T.left, index + 1, Coor)
        else:
            res = _decodedata(T.right, index + 1, Coor)
    return res

def decodedata(huffmanTree, dataIN):
    """
    Decode a string using the corresponding huffman tree into something more readable.
    """
    i = 0
    longeurString = len(dataIN)
    res = ""
    while i < longeurString:
        _res = ""
        char = (None, False)
        while not(char[1]) and i < longeurString:
            _res += dataIN[i]
            char = _decodedata(huffmanTree, 0, _res)
            i += 1
        res += char[0]
    return res
    pass

# Fonction récursive pour construire un HuffmanTree, elle prend en paramètre le code de l'arbre
# et l'index, quand l'index et trop loin elle s'arrête, quand elle rencontre un 1
# elle construit la feuille avec le caractère correspondant, sinon elle construit un fils gauche
# et débute un nouvelle récursion
def _decodetree(dataIN, index):
    if index >= len(dataIN):
        return
    elif dataIN[index] == "1":
        i = 1
        _res = ""
        while i <= 8:
            _res += dataIN [index + i]
            i += 1
        index += i
        _res = chr(_byteToInt(_res))
        return (bintree.BinTree(_res, None, None), index)
    else:
        B = bintree.BinTree(None, None, None)
        Couple = _decodetree(dataIN, index + 1)
        B.left = Couple[0]
        index = Couple[1]
        Couple = (_decodetree(dataIN, index))
        B.right = Couple[0]
        index = Couple[1]
    return (B, index)


def decodetree(dataIN):
    """
    Decodes a huffman tree from its binary representation:
        * a '0' means we add a new internal node and go to its left node
        * a '1' means the next 8 values are the encoded character of the current leaf
    """
    R = _decodetree(dataIN, 0)
    return R[0]
    pass


def frombinary(dataIN, align):
    """
    Retrieve a string containing binary code from its real binary value (inverse of :func:`toBinary`).
    """
    i = 0
    res = ""
    longueurString = len(dataIN)
    while i < longueurString - 1:
        res += _intToByte(ord(dataIN[i]))
        i += 1
    _res = _intToByte(ord(dataIN[i]))
    while align < 8:
        res += _res[align]
        align += 1
    return res
    pass


def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    DataCode = frombinary(data, dataAlign)
    TreeCode = frombinary(tree, treeAlign)
    HuffmamTree = decodetree(TreeCode)
    res = decodedata(HuffmamTree, DataCode)
    return res
    pass
