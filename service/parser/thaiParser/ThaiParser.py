from .data import districtSet,provinceSet,tambonSet
from attacut import tokenize

district = districtSet.district
province = provinceSet.province
tambon = tambonSet.tambon
def tokengen(addr):
  words = tokenize(addr)
  wordsNew = []
  k = 0
  skip = False
  for i in words:
    if skip:
      skip = False
      continue
    l = len(i)
    if l > 1 or i[0].isalnum():
      wordsNew.append(i) 
    if i == '/' and k > 0 and k < len(words)-2 and words[k-1].isnumeric() and words[k+1].isnumeric():
      wordsNew.pop()
      wordsNew.append(words[k-1]+i+words[k+1]) 
      skip = True
    k=k+1
  return wordsNew

def parse(add):
  # print("concated address for parse = ", add)
  tambonList = []
  provinceList = []
  districtList = []
#   possibleTambon = set()
#   possibleDistrict = set()
  words2 = tokenize(add)
  for i in words2:
    if i in province:
      provinceList.append(i)
    if i in district:
      districtList.append(i)
    if i in tambon:
      tambonList.append(i)
  return {"al3": tambonList,"al1": provinceList,"al2": districtList }

# print(parser("49/190 หมู่7, 12120, คลองหลวง/ Khlong Luang, ปทุมธานี/ Pathum Thani ปทุมธานี/ Pathum Thani 12120"))
# print(tokengen("7/31 ม.7 ต.คลองสอง อ.คลองหลวง ร้านค้า, 12120, คลองหลวง/ Khlong Luang, ปทุมธานี/ Pathum Thani"))
add = "บ้านเลข40/4ซอยรัชดาภิเษก32แยก7แขวงจันทรเกษมเขตจตุจักรกรุงเทพ10900, 10900, จตุจักร/ Chatuchak, กรุงเทพมหานคร/ Bangkok"
print(parse(add))
