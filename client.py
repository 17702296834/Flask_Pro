import requests
# user_info = {'name': 'wyh', 'password': '123'}
# json_data = {"a": 20, "b":40}
file_data = {
    'image': open('timg.png', 'rb')
}                                       
user_info = {'info': 'timg'}
r = requests.post("http://127.0.0.1:5000/upload", data=user_info, files=file_data)
print(r.text)
