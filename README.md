# Kubernetes configs for canonical websites

This repository contains the configuration files the Kubernetes deployments for some of [our websites](https://github.com/canonical-websites).

## Structure

We deploy our services into one of two namespaces:

- `staging`: Services for our staging servers (there's usually one per production website)
- `production`: Services for our production servers

### `services`

Both the [service](https://kubernetes.io/docs/concepts/services-networking/service/) and [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) config for a specific service are stored together in a single file at:

> `services/{primary-domain}.yaml`

E.g. the service and deployment settings for https://snapcraft.io are in `services/snapcraft.io.yaml`.

This config is then used to configure `snapcraft.io` services in both the `staging` and `production` namespace.

### `ingresses`

The [ingress resources](https://kubernetes.io/docs/concepts/services-networking/ingress/) are split into two folders, `ingresses/staging` and `ingresses/production`. These folders correspond to the namespaces in which those ingress resources will be applied, and there is one file per domain.

## Deploying

### Using create-project

When creating a new project you can either copy an existing projects service and ingress files. Then replace the config strings with the new project configs. 

Or, use `./create-project`. To auto generate the files for a new project. Run `./create-project project.name` and the tool will create the config files for you. 

For example:
`./create-project www.ubuntu.com`

Will create:
 - /service/www.ubuntu.com.yaml
 - /ingresses/staging/www.staging.ubuntu.com.yaml
 - /ingresses/production/www.ubuntu.com.yaml

### To deploy a new service

E.g. to deploy the snapcraft.io service to staging from scratch:

``` bash
# E.g. To deploy the snapcraft.io services to staging
export TAG_TO_DEPLOY=a264efb326485
envsubst < services/snapcraft.io.yaml | kubectl apply --namespace staging --filename -
```

### To update an existing service

Or to update an existing snapcraft.io service without changing the deployed image:

``` bash
# E.g. for snapcraft.io
export TAG_TO_DEPLOY=$(kubectl get deployment snapcraft-io -o jsonpath="{.spec.template.spec.containers[*].image}" | grep -P -o '(?<=:)[^:]*$')
envsubst < services/snapcraft.io.yaml | kubectl apply --namespace staging --filename -
```
