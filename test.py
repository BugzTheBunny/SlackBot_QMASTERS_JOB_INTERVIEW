import requests

ans = requests.post('http://127.0.0.1:5000/python-hub')
print(ans.content)