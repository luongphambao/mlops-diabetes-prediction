
#
```shell
cd k8s/helm/diabetes
helm upgrade --install diabetes .

```

```shell
k create ns model-serving
k port-forward svc/diabetes 30002:30000 -n model-serving
```
