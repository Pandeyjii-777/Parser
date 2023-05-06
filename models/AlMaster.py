class AlMaster:

    def __init__(self):
        self.createdAt = None
        self.countryCode = None
        self.companyId = None
        self.pincode = None
        self.al3 = None
        self.al2 = None
        self.al1 = None
        self.id = None
    def createObject(self, obj):
        self.id = obj[0]
        self.al1 = obj[3]
        self.al2 = obj[2]
        self.al3 = obj[1]
        self.pincode = obj[4]
        self.companyId = obj[5]
        self.countryCode = obj[6]
        self.createdAt = obj[7]


def createAlmasterFromArray(obj):
    arr = []
    for i in obj:
        al = AlMaster()
        al.createObject(i)
        arr.append(al)
    return arr