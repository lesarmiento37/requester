##!bin/bash
#export CONTAINER=$(docker ps | awk '{print $1}' | tail -n 1)
#echo $CONTAINER
#docker rm --force $CONTAINER
#docker rmi requester
#docker build -t requester ./
#docker run -d --name requests -p 80:80 requester
#sleep 2
#python3.8 test.py
#export CONTAINER_LOGS=$(docker ps | awk '{print $1}' | tail -n 1)
#echo $CONTAINER_LOGS
#docker logs $CONTAINER_LOGS
##python3.8 test.py

##################### BUILD STAGE ########################
IMAGE=$(kubectl get deploy/requester -o jsonpath="{..image}{'\n'}")
CURRENT_VERSION=$(echo $IMAGE| cut -c 24-27)
NEW_VERSION=$(echo "$CURRENT_VERSION + 1" | bc)
echo "Current Version $CURRENT_VERSION"
echo "New Version $NEW_VERSION"
docker build -t requester:v$NEW_VERSION ./
docker image tag requester:v$NEW_VERSION leonardos37/requester:v$NEW_VERSION
docker image push leonardos37/requester:v$NEW_VERSION
##################### TEST STAGE ########################
cd app
pytest unit-test.py
cd ..
##################### CODE ANALYSIS STAGE ###############
/home/leonardo/sonar/sonar-scanner-4.8.0.2856-linux/bin/sonar-scanner \
  -Dsonar.projectKey=requester \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=257611c1c2f83536b7934f7f51a6902c4329a7d2
#################### DEPLOY STAGE #######################
kubectl -n default --record deployment.apps/requester set image deployment.v1.apps/requester requester=lesarmiento37/requester:v$NEW_VERSION
#################### FINAL STAGE #######################
sleep 2
python3.8 test.py
