import requests

# Define the POST request data
data = {"message": "This is a test","to": "RUby Alvarez","from": "Rita Asturia","timeToLifeSec": 45}

# Define the headers
headers = {
    'X-JWT-KEY': 'rr4ToT3P92gVSomO',
    'X-Parse-REST-API-Key': '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c',
    'Content-Type': 'application/json'

}

# Send the POST request to minikube ip
response = requests.post("http://192.168.49.2:30007/devops/", data=data, headers=headers)
print(response.text)
