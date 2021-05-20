import json

payload_str = """

+HTTPCLIENT:190,{"coord":{"lon":116.3972,"lat":39.9075},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"base":"stations","main":{"temp":305.52,"feels_like":304.16,"temp_
+HTTPCLIENT:303,min":301.09,"temp_max":306.48,"pressure":995,"humidity":28},"visibility":10000,"wind":{"speed":3.98,"deg":190,"gust":3.44},"clouds":{"all":100},"dt":1621501757,"sys":{"type":2,"id":2000065,"country":"CN","sunrise":1621457730,"sunset":1621509998},"timezone":28800,"id":1816670,"name":"Beijing","cod":200}

OK

"""

# print(payload_str)

payload_list = payload_str.split('\n')
# print(payload_list)

json_str = ""
for line in payload_list:
    if line == "":
        continue
    elif line == "OK":
        continue
    else:
        if line.find("+HTTPCLIENT:") != -1:
            split_location = line.find(",")
            json_str += line[split_location + 1:]

print(json_str)

json_result = []
try :
    json_result = json.loads(json_str)
except :
    print("Json decode error")
print(json_result)
