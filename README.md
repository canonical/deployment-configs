# Kubernetes configs for canonical websites

## WIP

### Generate YAML files for a new site:

Production:

``` bash
# E.g. for canonical.com
helm template --values sites/canonical-com.yaml --output-dir ./output/canonical ./charts/production
```

Staging:
``` bash
# E.g. for canonical.com
helm template --values sites/canonical-com.yaml --output-dir ./output/canonical ./charts/staging
```
