import requests
import json

url = "https://api-laas.wanted.co.kr/api/preset/v2/chat/completions"

headers = {
    "accept": "application/json",
    "project": "PROMPTHON_PRJ_431",
    "apiKey": "79922959a824374c0e44c26e5d8dcee536842a4b279c196a1e4deb30f012829a",
    "Content-Type": "application/json"
}

payload = {
    "hash": "7705c62829e4a28c7dfdf5da1a8eaac8e96adefa32b3f53057e9372200727268",
    "params": {
        "task_assigned": "",
        "task_history": "",
        "assignee": "하도현/정보보안팀"
    },
    "model": "HCX-003",
    "messages": [
        {
            "role": "user",
            "content": "하도현이 하고 있는 일을 알려줘."
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.status_code)
print(response.json())