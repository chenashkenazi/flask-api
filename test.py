import requests

BASE = 'http://127.0.0.1:5000/'

response = requests.post(BASE + "order", {"drinks": [2055846, 2055838],
    "desserts": [2055835],
    "pizzas": []})
print(response.json())


'''
response = requests.post(BASE + "order", {"drinks": [2055846, 2055838],
    "desserts": [2055835],
    "pizzas": []})
'''