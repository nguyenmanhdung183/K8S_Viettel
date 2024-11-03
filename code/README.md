docker build -t manhdungnguyen/flask-app:latest .
docker push manhdungnguyen/flask-app:latest
kubectl apply -f app-deployment.yaml