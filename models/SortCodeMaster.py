class SortCodeMaster:

    def __init__(self):
        self.createdAt = None
        self.companyId = None
        self.sortCode = None
        self.pincode = None
        self.id = None

    def createObject(self, obj):
        self.id = obj[0]
        self.pincode = obj[1]
        self.sortCode = obj[2]
        self.companyId = obj[3]
        self.createdAt = obj[4]


def createSortCodeMasterFromArray(obj):
    arr = []
    for i in obj:
        scm = SortCodeMaster()
        scm.createObject(i)
        arr.append(scm)
    return arr
