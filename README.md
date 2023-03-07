# REQUESTER TOOL API REST
## PROJECT URL
https://github.com/lesarmiento37/tools/tree/main/requester
## PROJECT DESIGN
The first approach to solve this project is provision the code in python language, the neccesary libraries are fastapi for build the api, logger for logging purposes, typing and jwt for build secure methods.

The next step is testing the code inside a docker container provisioned by the Dockerfile and deployed with the commands:
```
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./app /app
```
With that we can test the api in a docker container in a local environment, this project is provisioned in a local computer.

Once the container is deployed, the test is carried out the following event:

```
data = {"message": "This is a test","to": "Leonardo Sarmiento Alcala","from": "Rita Asturia","timeToLifeSec": 45}
```
In the file test.py  the variables for the headers are defined.

For provision the entire project, the recommended arquitecture is in kubernetes (in this case is deployed in minikube), because we can provision many deployments to configure the load balancer and the sonarqube server.

Once installed minikube, the next step is provision through kubernetes manifest the following architecture:
![image](https://user-images.githubusercontent.com/17441125/223327458-83678a6e-46b5-41e4-a93b-3947c8237934.png)

Using this architecture it is possible define a CICD process through a bash script

## DEPLOYMENT PROCESS
The file deployment.sh have five stages: BUILD, TEST, CODE ANALYSIS. DEPLOY, FINAL

### BUILD STAGE
In this stage the process build a docker image with the existing code in the directory app/ and push an image to the dockerhub
![image](https://user-images.githubusercontent.com/17441125/223328515-5b4779f2-334f-44c6-8be0-b2f6e3447b0d.png)

### TEST STAGE
In this stage the process test the python function using pytest, there are two tests

![image](https://user-images.githubusercontent.com/17441125/223328561-2837eefd-4e88-48e6-9758-5d2bfe026fe2.png)

### CODE ANALYSIS STAGE
With the provisioned sonarqube server inside the same cluster, it is possible integrate with the code in the /app directory, Once the project is created and the SONAR_TOKEN is retrieved the the project is analyzed like this:

![image](https://user-images.githubusercontent.com/17441125/223328996-fd6751dc-6904-4ffa-a48e-8de683dd38b2.png)

### DEPLOY STAGE
In this stage of the pipeline, the image is updated in the kubernetes requester deployment

![image](https://user-images.githubusercontent.com/17441125/223329264-22f06d4b-33eb-45e1-8c30-12708174201a.png)

### FINAL STAGE
In this stage the output of the project is visualized by the event generated by the cpode test.py

![image](https://user-images.githubusercontent.com/17441125/223329604-9626aba4-7ab7-4f25-b300-4c9e4f693532.png)

## TESTING PROJECT
To check the different requirements of the project test are performed in different cases
### CORRECT EVENT AND HEADERS
With the input event:
```
data = {"message": "This is a test","to": "Leonardo Sarmiento Alcala","from": "Rita Asturia","timeToLifeSec": 45}
```
The application shows the next result:

![image](https://user-images.githubusercontent.com/17441125/223329604-9626aba4-7ab7-4f25-b300-4c9e4f693532.png)
### DIFFERENT EVENT AND HEADERS

With the input event:
```
data = {"message": "This is a test","to": "Ruby Alvarez","from": "Rita Asturia","timeToLifeSec": 45}
```
The application shows the next result:

![image](https://user-images.githubusercontent.com/17441125/223330325-ec304013-8630-4f3b-9873-f13bf0f192a5.png)

### INCORRECT X-Parse-REST-API-Key
![image](https://user-images.githubusercontent.com/17441125/223330560-931996a1-718f-4582-90c4-36069cc1142b.png)

### INCORRECT X-JWT-KEY
![image](https://user-images.githubusercontent.com/17441125/223330657-a8c2be26-5369-4bab-9896-1e1d51b83831.png)
### INCORRECT URL
![image](https://user-images.githubusercontent.com/17441125/223330772-f44f39fd-e11c-4392-baf8-0d9ab44987cb.png)
### INCORRECT UNIT TEST
With this testing parameters, the test fail
```
def test_converter_raw():
    raw_string = "message=This+is+a+test&to=Leonardo+Sarmiento&from=Rita+Asturia&timeToLifeSec=45"
    assert str_converter(raw_string) == {'message': 'This is a test','to': 'eonardo Sarmiento','from': 'Rita Asturia','timeToLifeSec': '45'}

def test_retrieve_name():
    raw_name = {'message': 'This is a test','to': 'Leonardo Sarmiento','from': 'Rita Asturia','timeToLifeSec': '45'}
    assert name_provider(raw_name) == {"message":"Hello Leonardo armiento, your message will be send"}

```
![image](https://user-images.githubusercontent.com/17441125/223331307-a0f0c4b7-9a90-4d9f-8755-36ccb03e4ef8.png)

## SONAR SECURITY OUTPUT
In that case sonar shows a security vulnerability because the code have an exposed endpoint:
![image](https://user-images.githubusercontent.com/17441125/223331709-36cbca46-5d70-4223-9384-6ccfadf117a1.png)


