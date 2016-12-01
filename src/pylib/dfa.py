class cNode:

    def __init__(self):
        self.children = None


# The encode of word is UTF-8
# The encode of message is UTF-8
class cDfa:

    def __init__(self, lWords):
        self.root = None
        self.root = cNode()
        for sWord in lWords:
            self.addWord(sWord)

    # The encode of word is UTF-8
    def addWord(self, word):
        node = self.root
        iEnd = len(word)-1
        for i in range(len(word)):
            if node.children is None:
                node.children = {}
                if i != iEnd:
                    node.children[word[i]] = (cNode(), False)
                else:
                    node.children[word[i]] = (cNode(), True)

            elif word[i] not in node.children:
                if i != iEnd:
                    node.children[word[i]] = (cNode(), False)
                else:
                    node.children[word[i]] = (cNode(), True)
            # word[i] in node.children:
            else:
                if i == iEnd:
                    Next, bWord = node.children[word[i]]
                    node.children[word[i]] = (Next, True)

            node = node.children[word[i]][0]

    def isContain(self, sMsg):
        root = self.root
        iLen = len(sMsg)
        for i in range(iLen):
            p = root
            j = i
            while (j < iLen and p.children is not None
                    and sMsg[j] in p.children):
                p, bWord = p.children[sMsg[j]]
                if bWord:
                    return True
                j = j + 1
        return False

    def filter(self, sMsg):
        lNew = []
        root = self.root
        iLen = len(sMsg)
        i = 0
        bContinue = False
        while i < iLen:
            p = root
            j = i
            while (j < iLen and p.children is not None
                    and sMsg[j] in p.children):
                p, bWord = p.children[sMsg[j]]
                if bWord:
                    # 关键字替换
                    # lNew.append(u'*' * (j-i+1))
                    lNew.append(u'[哔~]')
                    i = j+1
                    bContinue = True
                    break
                j = j+1
            if bContinue:
                bContinue = False
                continue
            lNew.append(sMsg[i])
            i = i+1

        return ''.join(lNew)
