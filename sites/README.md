# Valid properties

List of possible values that can be used

## name
**Type:** String

This property will be used for all the Kubernetes metadata names. If not specified by default it will be the domain name, replacing the dots with dashes.

Example:
```
name: threesixty-canonical-com
staging:
  name: threesixty-staging-canonical-com
```

## domain
**(Mandatory)**

**Type:** String

This property define the project domain, it will be used for the Service, Deployment and Ingress objects.

Example:
```
domain: canonical.com
```

## image
**(Mandatory)**

**Type:** String

Set the Docker image you want to use.

Example:
```
image: prod-comms.docker-registry.canonical.com/canonical.com
```

## replicas

**Type:** Int

**Default:** 5

Number of replicas to use.

Example:
```
replicas: 2
```

## containerPort

**Type:** Int

**Default:** 80

Port to expose from the container.

Example:
```
containerPort: 8080
```

## useProxy

**Type:** Boolean

**Default:** True

This will use our ConfigMap object "proxy-config", you can take a look to this object here: `configmaps/proxy-config.yaml`

Example:
```
useProxy: False
```

## readinessPath

**Type:** String

**Default:** /_status/check

Define the URL path to do a readiness probe.

Example:
```
readinessPath: /
```

## memoryLimit

**Type:** String

**Default:** 256Mi

It will define the container memoryLimit limit.

Example:
```
memoryLimit: 512Mi
```

## noTls

**Type:** Boolean

**Default:** False

It will not add any TLS secret in the Ingress object.

Example:
```
noTls: True
```

## env

This property is for environment related configurations. Here you can set the [name](#name-1) and the [value](#value) or [secretKeyRef](#secretKeyRef).

### name

**Type:** String

Example:
```
env:
  - name: SENTRY_DSN
```

### value

**Type:** String

Example:
```
env:
  - name: SENTRY_DSN
    value: https://426397ba83be483a8a8d1ed92b0f0623@sentry.is.canonical.com//17
```

### secretKeyRef
#### key & name

**Type:** String

Example:
```
  - name: SEARCH_API_KEY
    secretKeyRef:
      key: google-custom-search-key
      name: google-api
```

## extraHosts
### domain

**Type:** String

Domains to be included in the Ingress object.

Example:
```
extraHosts:
  - domain: docs.staging.jujucharms.com
```

### useParentTLS

**Type:** Boolean

**Default:** False

Use the same TLS name for this domain.

Example:
```
extraHosts:
  - domain: cloud-init.org
    useParentTLS: True
```

## routes

**Type:** Array

It will add paths in the Ingress file and it will generate a Service and Deployment for each one. Because of this it is possible to set any main properties under this level.

### path

**Type:** String

Example:
```
routes:
  - path: /blog
    image: prod-comms.docker-registry.canonical.com/ubuntu.com
    memoryLimit: 512Mi
```

## nginxConfigurationSnippet

**Type:** String

Using this annotation you can add additional configuration to the NGINX location.

Example:
```
nginxConfigurationSnippet: |
  if ($host != 'canonical.com' ) {
    rewrite ^ https://canonical.com$request_uri? permanent;
  }
  more_set_headers "Link: <https://assets.ubuntu.com>; rel=preconnect; crossorigin, <https://assets.ubuntu.com>; rel=preconnect";
```

## production
Under this level you can overwrite any of the above mentioned properties for this environment.

Example:
```
production:
  extraHosts:
    - domain: cloud-init.org
```

## staging
Under this level you can overwrite any of the above mentioned properties for this environment.

Example:
```
staging:
  nginxConfigurationSnippet: |
    more_set_headers "X-Robots-Tag: noindex";
```
