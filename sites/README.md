# Valid properties

List of possible values that can be used

## name
**(Mandatory)**

**Type:** String

This property will be used mainly for all the Kubernetes metadata name, it will also be used to set some properties as a default value if they have not been defined as tlsSecretName.

Example:
```
name: canonical-com
```

## domain
**(Mandatory)**

**Type:** String

This property define the project domain, it will be used for the Service, Deployment and Ingress objects.

Example:
```
domain: canonical.com
```

## noIngress

**Type:** Boolean

**Default:** False

When this property is set to true, the Ingress object will be empty.

Example:
```
noIngress: true
```

## container
**(Mandatory)**

This property is for container related configurations. Here you can set the [image](#image) and the [tag](#tag).

### image
**(Mandatory)**

**Type:** String

Set the Docker image you want to use.

Example:
```
container:
    image: prod-comms.docker-registry.canonical.com/canonical.com
```

### tag

**Type:** String

**Default:** latest

You can specify the tag you want to use with the image.

Example:
```
container:
    image: prod-comms.docker-registry.canonical.com/canonical.com
    tag: a264efb326485
```

## wwwPrefixHost

**Type:** Boolean

**Default:** True

When True it will include an extra host with the www prefix to the Ingress object.

Example:
```
wwwPrefixHost: false
```

## tlsSecretName

**Type:** String

**Default:** {name}-tls

Here you can define the name of the TLS secret for the domain. This name will be used for the www prefix host if `wwwPrefixHost` is True.

Example:
```
tlsSecretName: cloud-init-org-tls
```

## useSquid

**Type:** Boolean

**Default:** False

This will use our ConfigMap object "proxy-config", you can take a look to this object here: `configmaps/proxy-config.yaml`

Example:
```
useSquid: True
```

## readinessPath

**Type:** String

**Default:** /_status/check

Define the URL path to do a readiness probe.

Example:
```
readinessPath: /
```

## readinessPeriodSeconds

**Type:** Int

**Default:** 5

How often (in seconds) to perform the probe. Default to 5 seconds. Minimum value is 1.

Example:
```
readinessPeriodSeconds: 10
```

## readinessSuccessThreshold

**Type:** Int

**Default:** 1

Minimum consecutive successes for the probe to be considered successful after having failed. Defaults to 1. Must be 1 for liveness. Minimum value is 1.

Example:
```
readinessSuccessThreshold: 5
```

## readinessTimeoutSeconds

**Type:** Int

**Default:** 3

Number of seconds after which the probe times out. Defaults to 3 second. Minimum value is 1.

Example:
```
readinessTimeoutSeconds: 5
```

## memory

**Type:** String

**Default:** 256Mi

It will define the container memory limit.

Example:
```
memory: 512Mi
```

## envSecrets

This property is for environment related configurations. Here you can set the [name](#name-1) and the [value](#value) or [secretKeyRef](#secretKeyRef).

### name

**Type:** String

Example:
```
envSecrets:
  - name: SENTRY_DSN
```

### value

**Type:** String

Example:
```
envSecrets:
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
### host

**Type:** Array

Domains to be included in the Ingress object.

Example:
```
extraHosts:
  - host:
    - docs.staging.jujucharms.com
```

### tlsSecret

**Type:** String

Use a specific TLS name for the domains.

Example:
```
  extraHosts:
    - host:
      - docs.staging.jujucharms.com
      tlsSecret: docs-staging-jujucharms-com-tls
```

### noTls

**Type:** Boolean

The hosts will not be included in the TLS section of the Ingress object.

Example:
```
- host:
  - ubuntu.net
  noTls: true
```

## nginxConfig

**Type:** String

Using this annotation you can add additional configuration to the NGINX location.

Example:
```
nginxConfig:  |
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
    - host:
      - cloud-init.org
      - www.cloud-init.org
```

## staging
Under this level you can overwrite any of the above mentioned properties for this environment.

Example:
```
staging:
  nginxConfig: |
    more_set_headers "X-Robots-Tag: noindex";
```
