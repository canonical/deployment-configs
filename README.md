# Kubernetes configs for canonical websites

This repository contains the configuration files the Kubernetes deployments for some of [our websites](https://github.com/canonical-websites).

We are using [jinja2](https://jinja.palletsprojects.com/) as a template system for our configurations. All the template values for our projects can be found under the sites folder.

## Structure

We deploy our services into one of two namespaces:

- `staging`: Services for our staging servers (there's usually one per production website)
- `production`: Services for our production servers

### Template system
All configurations for our projects can be found under the sites folder. Using the konf.py script, we generate the following Kubernetes objects:
- service
- deployment
- ingress

E.g.:
``` bash
./konf.py staging sites/canonical.com.yaml
```

## Deploying

### Using create-project

When creating a new project, you can either copy an existing projects values file and modify the file as you want. Here is a document explaining all the possibles values:

- [Values file manual](sites/README.md)

Or use `./create-project`. To auto-generate the files for a new project. Run `./create-project project.name` and the tool will create the config files for you.

For example:
`./create-project new-site.com`

Will create:
 - /sites/new-site.com.yaml

### To deploy a new service

E.g. to deploy the snapcraft.io service to staging from scratch:

``` bash
# E.g. To deploy the snapcraft.io services to staging
./konf.py staging sites/snapcraft.io.yaml | kubectl apply --filename -
```

E.g. to deploy a specific docker image

``` bash
# E.g. To deploy the snapcraft.io services to staging
./konf.py staging sites/snapcraft.io.yaml --tag a264efb326485 | kubectl apply --filename -
```

### To update an existing service

Or to update an existing snapcraft.io service without changing the deployed image:

``` bash
# E.g. for snapcraft.io
TAG_TO_DEPLOY=$(kubectl get deployment snapcraft-io --namespace staging -o jsonpath="{.spec.template.spec.containers[*].image}" | grep -P -o '(?<=:)[^:]*$')

./konf.py staging sites/snapcraft.io.yaml --tag $TAG_TO_DEPLOY | kubectl apply --filename -
```
