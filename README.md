# UDP Echo server including source ip address and port
A simple UDP echo server that responds back whatever data the client sends
as well as client source ip address and source port.

## Running with docker
`docker run -d -p 33333:33333/udp -p 33332 dlee116/packet-mirror:latest`

## Running on Kubernetes
```
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-lb.yaml
```
