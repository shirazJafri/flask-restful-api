import requests

BASE = "http://127.0.0.1:5000/"


data = [
    {"name": "World's Most Viewed TikToks!", "likes": 1200000, "views": 34000000},
    {"name": "Habib Jalib - Mainay Uss Say Yeh Kaha - Laal", "likes": 3500, "views": 533418},
    {"name": "Better Call Saul: Ethics Are Strange", "likes": 8400, "views": 255761}
]

for i in range(len(data)):
    response_PUT= requests.put(BASE + 'video/' + str(i), data[i])
    print(response_PUT.json())

input()

response_DEL = requests.delete(BASE + 'video/2')
# Not writing .json() because the object being returned in handling the DELETE request is not JSON-serializable.
print(response_DEL)

input()

response_GET = requests.get(BASE + 'video/2')
print(response_GET.json())

input()

response_GET = requests.get(BASE + 'video/1')
print(response_GET.json())


