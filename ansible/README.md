# How-to Guide

## 1. Spin up your instance

```bash
cd deploy_jenkins
ansible-playbook create_compute_instance.yaml
```

## 2. Install Docker and Jenkins

Update the IP of the newly created instance to the `inventory` file, then run the following commands:

```bash
cd deploy_jenkins
ansible-playbook -i ../inventory deploy_jenkins.yml
```

## 3. Install Kubernetes plugin

Please install the Kubernetes plugin and set up a connection to GKE as guidance on the lesson.

Don't forget to grant permissions to the service account which is trying to connect to our cluster by the following command:

```shell
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole=cluster-admin --user=system:anonymous

kubectl create clusterrolebinding cluster-admin-default-binding --clusterrole=cluster-admin --user=system:serviceaccount:default:default
```
