from string import Template
import requests
import json

print("============================== start GeoSmartEls.py content =============================")


def get_json_body_by_elsQuery(address, pincode, Obj):
    notEmpty = False
    key=list(Obj.keys())
    keyLen = len(key)
    print("keys of Obj are ", key, " and it's an array")
    print("index number of key name (", key[keyLen-3]," ) is ", key.index(key[keyLen-3]))
    print("value of key name of last index in keys is " , Obj[key[keyLen-1]])
     
    while(keyLen>0):
      if(len(Obj[key[keyLen-1]])>0):
        if(notEmpty):
          if(type(Obj[key[keyLen-1]]) is list): 
            key[keyLen-1] = '{ "terms": { "' + key[keyLen-1] + '" : '+ json.dumps(Obj[key[keyLen-1]]) +'}},'
          else:
            key[keyLen-1] = '{ "match": { "' + key[keyLen-1] + '" : "'+ Obj[key[keyLen-1]] +'"}},'
        else:
          if(type(Obj[key[keyLen-1]]) is list): 
            key[keyLen-1] = '{ "terms": { "' + key[keyLen-1] + '" : '+ json.dumps(Obj[key[keyLen-1]]) +'}}'
          else:
            key[keyLen-1] = '{ "match": { "' + key[keyLen-1] + '" : "'+ Obj[key[keyLen-1]] +'"}}'
        notEmpty = True     
      else:
        key[keyLen-1] = ""
      keyLen = keyLen -1


    t = Template("""
                    {
                      "query": 
                        { "bool": 
                            { "must": 
                              [
                                { "match": 
                                  {
                                    "address": "${address}"
                                  }
                                }
                              ],
                              "filter":
                              [
                                { "match": 
                                  {
                                    "pincode": "${pincode}"
                                  }
                                }
                              ],
                              "should": 
                              [
                                  ${al1}
                                  ${al2}
                                  ${al3}
                                  ${sortcode}
                                  ${keyword}
                              ]
                            }
                        },
                      "size":1
                    }""")

    return t.substitute(address=address, pincode=pincode, keyword = key[keyLen-1],  sortcode = key[keyLen-2],  al3 = key[keyLen-3],  al2 = key[keyLen-4],  al1 = key[keyLen-5])
     

def get_from_es_lns(Obj, resultOfLatLng, key):
    uri = "http://localhost:9200/surya/_search"
    headers = {
        'Content-Type': 'application/json',
    }

    resp_text=''
    try:
     resp_text = requests.get(uri, data=get_json_body_by_elsQuery(Obj["address"], Obj["pincode"], Obj["add"]).encode('utf-8'), headers=headers)
    except requests.exceptions.ConnectionError:
     requests.status_code = "Connection refused"

   
    print("")
    print("This is get_json_body(df)", get_json_body_by_elsQuery(Obj["address"], Obj["pincode"], Obj["add"]))
    print("this is resp_text.json()", resp_text.json())
    resp = resp_text.json()
    if "hits" in resp.keys():
      if resp and resp["hits"] and len(resp["hits"]["hits"])>0:
          es_lat = resp["hits"]["hits"][0]["_source"]["lat"]
          es_lng = resp["hits"]["hits"][0]["_source"]["lng"]
          es_score = resp["hits"]["hits"][0]["_score"]
          resultOfLatLng[key] = {"lat":str(es_lat), "lng":str(es_lng), "_score":str(es_score)}
          print("resultOfLatLng[key] = ", resultOfLatLng[key])
          return
    resultOfLatLng[key] = {"lat":None, "lng":None, "_score":"0"}
    # print("resultOfLatLng[key] = ", resultOfLatLng[key])





print("==============================  End  GeoSmartEls.py content =============================")


