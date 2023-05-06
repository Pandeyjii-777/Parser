from service.Connections import *
from .parser.thaiParser import ThaiParser
from service.AddressParse import *
import time
import asyncio
from threading import Timer
from service.GeoSmartEls import *


def getAddressByCompanyIdAndHubId(company_id, hub_id, user_id):
    get_pincode='''SELECT pincode FROM hub_pincode_mapping WHERE company_id=(%s) AND hub_id=(%s)'''
    cur.execute(get_pincode, (company_id, hub_id))

    temp=cur.fetchone()[0]
    if (len(temp)==0): return []
    print("temp = ", temp)

    
    get_address="SELECT address, address_id, pincode FROM non_labeled_address WHERE company_id=(%s) AND pincode IN (%s) and processing_start_time <= NOW() -INTERVAL '1 HOUR';"

    cur.execute(get_address, (company_id, temp))
   
    # BEGIN; LOCK TABLE non_labeled_address IN ACCESS EXCLUSIVE MODE;

    count = 0
    result = {}
    address=[]
    idList=[]
    data = {}
    data['parserName'] = "thaiParser"
    data['address'] ={}
    returnResult = []

    print("data[parserName] = thaiParser = ", data["parserName"])

   
    # it return the first 30 rows and the after calling again it fetch next 30 rows, and so on;
    add=""
    def fetchNext(): 
      return cur.fetchmany(70)

    fetchCount = 0
    while(count != 10 and fetchCount < 4):
        fetchCount = fetchCount + 1
        print("fetchCount = ", fetchCount, count)
        add=fetchNext()
        address.clear()
        ids = []
        for a in add:
            address.append(a[0])
            ids.append(a[1])
            data["address"][a[1]] = {}
            data["address"][a[1]]["address"] = a[0]
            data["address"][a[1]]["pincode"] = a[2]
            data["address"][a[1]]["country"] = "th"
        result = normalParse(data)
        for id in ids:
        # print("New parsed address status and id", secondResult[id]["RelationshipCheck"], secondResult[id], )
          if(result[id]["RelationshipCheck"]):
             count+=1
             idList.append(id)
             returnResult.append(result[id])
          if(count==10):
            break

    update = 'UPDATE non_labeled_address SET processing_start_time = NOW(), user_id=(%s) WHERE company_id=(%s) AND address_id IN ('+ ','.join(map(str, idList)) + ')'
    cur.execute(update, (user_id, company_id))

    conn.commit()

    print("Count = ", count)
    return returnResult



def getLatAndLng(data):
# here parserName will be get by company_Id that will be in header;
    parserName="thaiParser"    

    # Step-1 Concat address of each test;
    address_testes = {}
    address_testes['parserName'] = parserName
    address_testes['address'] = {}
    resultOfLatLng = {}

    for testes in data["addresses"]:
        starting = True
        concat_address = ''
        # return testes #result= "test1"
        # return data["addresses"][testes] #result= value of "test1"
        if(data["addresses"][testes]['line1']!=""):
            if(starting):
              concat_address+=data["addresses"][testes]['line1']
              starting = False
            else:
              concat_address+= " " + data["addresses"][testes]['line1']
        if(data["addresses"][testes]['line2']!=""):
            if(starting):
              concat_address+=data["addresses"][testes]['line2']
              starting = False
            else:
              concat_address+= " " + data["addresses"][testes]['line2']
        if(data["addresses"][testes]['landmark']!=""):
            if(starting):
              concat_address+=data["addresses"][testes]['landmark']
              starting = False
            else:
              concat_address+= " " + data["addresses"][testes]['landmark']
        if(data["addresses"][testes]['pincode']!=""):
            if(starting):
              concat_address+=data["addresses"][testes]['pincode']
              starting = False
            else:
              concat_address+= " " + data["addresses"][testes]['pincode']
        if(data["addresses"][testes]['country']!=""):
            if(starting):
              concat_address+=data["addresses"][testes]['country']
              starting = False
            else:
              concat_address+= " " + data["addresses"][testes]['country']
         
        print("Concted address is = ", concat_address)
        
        
        #Step-3, make an object that contain parserName, concat_address as address, pincode, country for each test;
        address_testes['address'][testes] = {}
        address_testes['address'][testes]['address'] = concat_address
        address_testes['address'][testes]['pincode'] = data["addresses"][testes]['pincode']
        address_testes['address'][testes]['country'] = data["addresses"][testes]['country']

    print("***********************************************************************")
    # Finaly send that whole address_testes for parse and return the parse for all testes in address; 
    # here address_testes['address] is an array of object
    parsed_address_testes = normalParse(address_testes)

    #Step-4, Here Elastic Search function will be call for search the value of attributes(al1, al2,..) of parsed_address 
    # and match for concated address and pincode in  a table 
    #And return lat, lng for that address in table

   # Either here i have use for loop or in elastic search but in elastic search for loop can be compicated;
    for key in parsed_address_testes:
        print("parsed_address_testes[key] = ", parsed_address_testes[key])
        print("parsed_address_testes[key]['address'] = ", parsed_address_testes[key]['address'])
        print("parsed_address_testes[key]['parsed_address']['al1'] = ", parsed_address_testes[key]['parsed_address']['al1'])
        
        Obj = {}
        Obj["address"] = parsed_address_testes[key]['address']
        Obj["add"] = {}
        Obj["add"]["al1"] = ''
        Obj["add"]["al2"] = ''
        Obj["add"]["al3"] = ''
        Obj["add"]["sortcode"] = ''
        Obj["add"]["keyword"] = ''
        Obj["pincode"] = ''
        if 'al1' in  parsed_address_testes[key]['parsed_address']:
            # parsed_address_testes[key]['parsed_address']['al1']=["Bihar", "Up", "Punjab"]
            Obj["add"]["al1"] = parsed_address_testes[key]['parsed_address']['al1']
        if 'al2' in  parsed_address_testes[key]['parsed_address']:
            Obj["add"]["al2"] = parsed_address_testes[key]['parsed_address']['al2']
        if 'al3' in  parsed_address_testes[key]['parsed_address']:
            Obj["add"]["al3"] = parsed_address_testes[key]['parsed_address']['al3']
        if 'sortcode' in  parsed_address_testes[key]['parsed_address']:
            Obj["add"]["sortcode"] = parsed_address_testes[key]['parsed_address']['sort_code']
        if 'keyword' in  parsed_address_testes[key]['parsed_address']:
            Obj["add"]["keyword"] = parsed_address_testes[key]['parsed_address']['keyword']
        if 'pincode' in  parsed_address_testes[key]['parsed_address']:
            Obj["pincode"] = parsed_address_testes[key]['parsed_address']['pincode']
        print("=======================================================================================")
        print(Obj)
        get_from_es_lns(Obj, resultOfLatLng, key)
       
    print("Lat, lng for All for parsed address = ", resultOfLatLng)

    return resultOfLatLng


def updateAndSave(parsed_address, company_id, user_id):
    for item in parsed_address:
        item["company_id"] = company_id
        item["user_id"] = user_id
    
    producer.send('address', parsed_address)
    return parsed_address

def parseAddress(addr,company_id,country_code):
    print(ThaiParser.parse("บ้านเลข40/4ซอยรัชดาภิเษก32แยก7แขวงจันทรเกษมเขตจตุจักรกรุงเทพ10900, 10900, จตุจักร/ Chatuchak, กรุงเทพมหานคร/ Bangkok"))















