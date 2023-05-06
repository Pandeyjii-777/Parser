from .parser.thaiParser import ThaiParser
from service.Connections import *
from models.AlMaster import *
from models.SortCodeMaster import *
from service.AddressService import *


def get_parser(parserName):
    if parserName == "thaiParser":
        thaiParser = ThaiParser
        return thaiParser
    elif parserName == "spanishParser":
        pass
    else:
        pass

priority = ['pincode','al3','al2']


def normalParse(data):
    parser = get_parser(data["parserName"])
    # print("data[parserName] = ", data["parserName"])
    parsed_address = {}
    for k in data["address"]:
        d = data["address"][k]
        # print("Address to be parse = ", d["address"])
        parsed_addr= parser.parse(d["address"])
        parsed_addr["pincode"] = d["pincode"]
        parsed_address[k] = { 'parsed_address': parsed_addr, 'address': d["address"], 'pincode': d["pincode"], 'country': d['country'] }
        # print(parsed_address[k])

    relationshipCheck(parsed_address)   

    return parsed_address

def relationshipCheck(parsedAddress):
    for k in parsedAddress:
        d = parsedAddress[k]
        alRels = None
        for i in priority:

            if i in d:
                print(i + " Entered")
                val2 = None
                # if i == "sort_code" and "pincode" in d:
                #     val2 = d["pincode"]
                alRels = getRelations(i,d[i],val2,1,'th')
                break
                # if rel is None:
                #     continue
        alRelArr = []
        for i in alRels:
            found = True
            if 'al1' in d["parsed_address"] and len(d["parsed_address"]['al1']) != 0 and d["parsed_address"]['al1'][0] != i.al1:
                found = False
            if 'al2' in d["parsed_address"] and len(d["parsed_address"]['al2']) != 0 and d["parsed_address"]['al2'][0] != i.al2:
                found = False
            if 'al3' in d["parsed_address"] and len(d["parsed_address"]['al3']) != 0 and d["parsed_address"]['al3'][0] != i.al3:
                found = False
            if found:
                alRelArr.append(i)

        if len(alRelArr) == 0:
            d["RelationshipCheck"] = False
        else:
            d["RelationshipCheck"] = True
        pincodes = []
        for i in alRelArr:
            if i.pincode != '' or i.pincode is not None:
                pincodes.append(i.pincode)
        d['sortCodeRelCheck'] = 'NA'
        # alRelArrRes = alRelArr
        if 'sort_code' in d:
            sortCodePincodes = getRelations('sort_code', d["sort_code"],pincodes,1,'th')
            if len(sortCodePincodes) == 0:
                d['sortCodeRelCheck'] = 'Failed'
            else:
                d['sortCodeRelCheck'] = 'Success'
        


def getRelations(levelName, value, value2, companyId, countryCode):
    curr = conn.cursor()
    if levelName == 'sort_code':
        pincodesString = "("
        first = True
        for i in value2:
            if first:
                pincodesString = pincodesString + "'"+str(i)+"'"
            else:
                pincodesString = pincodesString + ",'"+str(i)+"'"
        pincodesString += ")"

        query = "Select * from sort_code_master where pincode in {0} and company_id ={1} and sort_code={2}".format(pincodesString,companyId,value)
        curr.execute(query)
        res = curr.fetchall()
        ret = createSortCodeMasterFromArray(res)
        pincodes = []
        for i in ret:
            pincodes.append(i.pincode)
        return pincodes
    elif levelName == 'keyword':
        pass
    else:
        query = "Select * from al_master where company_id ='{0}' and country_code = '{1}' and {2} = '{3}'".format(
            companyId, countryCode,levelName, value)
        curr.execute(query)
        res = curr.fetchall()
        ret = createAlmasterFromArray(res)
        # for row in res:
        #     print("ID = ", row[0])
        #     print("NAME = ", row[1])
        #     print("ADDRESS = ", row[2])
        #     print("SALARY = ", row[3], "\n")
        return ret
        # print(res)
        #
        # if (len(res) == 0): return None
        # return res

# def countValidRelation(rel,)
