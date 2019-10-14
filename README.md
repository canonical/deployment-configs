# Kubernetes configs for canonical websites

## WIP

Projects k8s configurations using Jinja2-CLI as a template system. This repo is not ready, missing all the project configurations and the scripts to generate new project configurations and qa.

### Generate YAML files for a new site

Production:

``` bash
# E.g. for canonical.com
jinja2 templates/production/service.yaml sites/canonical-com/production.yaml > manifests/canonical-com/production/service.yaml

jinja2 templates/production/deployment.yaml sites/canonical-com/production.yaml > manifests/canonical-com/production/deployment.yaml

jinja2 templates/production/ingress.yaml sites/canonical-com/production.yaml > manifests/canonical-com/production/ingress.yaml
```

Staging:
``` bash
# E.g. for canonical.com
jinja2 templates/staging/service.yaml sites/canonical-com/staging.yaml > manifests/canonical-com/staging/service.yaml

jinja2 templates/staging/deployment.yaml sites/canonical-com/staging.yaml > manifests/canonical-com/staging/deployment.yaml

jinja2 templates/staging/ingress.yaml sites/canonical-com/staging.yaml > manifests/canonical-com/staging/ingress.yaml
```

### Apply kubernetes manifests

Run local QA:
``` bash
# E.g. for canonical.com
cat sites/canonical-com/production.yaml qa-overrides.yaml | jinja2 templates/production/service.yaml | microk8s.kubectl apply -f -

cat sites/canonical-com/production.yaml qa-overrides.yaml | jinja2 templates/production/deployment.yaml | microk8s.kubectl apply -f -

cat sites/canonical-com/production.yaml qa-overrides.yaml | jinja2 templates/production/ingress.yaml | microk8s.kubectl apply -f -
```

Deploy apply:
``` bash
# E.g. for canonical.com
microk8s.kubectl apply --recursive --filename manifests/canonical-com/production
```
