import requests

result = requests.get("http://www.naver.com")
print(result.text)