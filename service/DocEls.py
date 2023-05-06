# import requests
# import json



# #  Create index in elasticSearch database start here ;
# index_format = {
#   "settings": {
#     "number_of_shards": 1
#   },
#   "mappings": {
#     "properties": {
#       "address": { "type": "text" },
#       "al1": { "type": "text" },
#       "al2": { "type": "text" },
#       "al3": { "type": "text" },
#       "sortcode": { "type": "text" },
#       "keyword": { "type": "text" },
#       "pincode": { "type": "text" },
#       "lat": { "type": "text" },
#       "lng": { "type": "text" }
#     }
#   }
# }


# print(index_format)

# def create_index_els(my_index):
#     uri = f"http://localhost:9200/{my_index}"
#     headers = {
#         'Content-Type': 'application/json'
#     } 
    
#     index_created = ''
#     try:
#      index_created = requests.put(uri, data=json.dumps(index_format), headers=headers)
#     except requests.exceptions.ConnectionError:
#      requests.status_code = "Connection refused"

#     print("response of index_created = ", index_created)

# # index_name should be lowercase latter;
# create_index_els("pandey")

# #  Create index in elasticSearch database end here ;





# # Upload the data to doc of your created index in elasticSearch database start here ;

# dataAttr = ["address", "al1", "al2", "al3", "sortcode", "keyword", "pincode", "lat", "lng"]

# allData = [
# ["Bihar, Kaimur(Bhabhua), Naraw", "Bihar", "Kaimur", "Naraw", "sort3", "BKN", "821106", "864.23", "4.344"],
# ["Bihar, Kaimur(Bhabhua), Katara", "Bihar", "Kaimur", "Katara", "sort4", "BKK", "821107", "64.23765", "5.89344"]
# ]


# print("len(allData) = ", len(allData), allData[0])

# def upload_data_to_els_one_by_one(obj, index, index_name):
#     uri = f"http://localhost:9200/{index_name}/_doc/{index}"
#     headers = {
#         'Content-Type': 'application/json'
#     } 
    
#     uploaded = ''
#     try:
#      uploaded = requests.put(uri, data=json.dumps(obj), headers=headers)
#     except requests.exceptions.ConnectionError:
#      requests.status_code = "Connection refused"

#     print("response of uploaded = ", uploaded)


# def upload_data_format(data, dataAttributes, index, index_name):
#     obj = {}
#     for key in range(len(dataAttributes)):
#       obj[dataAttributes[key]] = data[key]

#     print("object is ", obj)
#     print("object is ", json.dumps(obj))
#     upload_data_to_els_one_by_one(obj, index, index_name)


# def upload_data_to_els(alldata, index_name):
#     for i in range(len(alldata)):
#       print("i = ", alldata[i])
#       upload_data_format(alldata[i], dataAttr, i, index_name)
    


# upload_data_to_els(allData, "pandey")

# # Upload the data to doc of your created index in elasticSearch database end here ;


        


