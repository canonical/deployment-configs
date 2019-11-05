# Valid properties

List of possible values that can be used

## name
(Mandatory)
Type: String
```
name: canonical-com
```

## domain
(Mandatory)
Type: String
```
domain: canonical.com
```

## noIngress
Type: Boolean
```
noIngress: true
```

## container
(Mandatory)

### image
(Mandatory)
Type: String

```
container:
    image: prod-comms.docker-registry.canonical.com/canonical.com
```

### tag
Type: String
Default: latest
```
container:
    image: prod-comms.docker-registry.canonical.com/canonical.com
    tag: a264efb326485
```

## wwwPrefixHost
Type: Boolean
Default: True
```
wwwPrefixHost: false
```

## tlsSecretName
Type: String
Default: {name}-tls
```
tlsSecretName: cloud-init-org-tls
```

## useSquid
Type: Boolean
Default: False
```
useSquid: True
```

## readinessPath
Type: String
Default: /_status/check
```
readinessPath: /
```

## readinessPeriodSeconds
Type: Int
Default: 5
```
readinessPeriodSeconds: 10
```

## readinessSuccessThreshold
Type: Int
Default: 1
```
readinessSuccessThreshold: 5
```

## readinessTimeoutSeconds
Type: Int
Default: 3
```
readinessTimeoutSeconds: 5
```

## memory
Type: String
Default: 256Mi
```
memory: 512Mi
```

## envSecrets
### name
Type: String

```
envSecrets:
  - name: SENTRY_DSN
```
### value
Type: String

```
envSecrets:
  - name: SENTRY_DSN
    value: https://426397ba83be483a8a8d1ed92b0f0623@sentry.is.canonical.com//17
```

### secretKeyRef
#### key & name
Type: String

```
  - name: SEARCH_API_KEY
    secretKeyRef:
      key: google-custom-search-key
      name: google-api
```

## extraHosts
### host
Type: String

```
- host:
  - docs.staging.jujucharms.com
```
### tlsSecret
Type: String

```
  extraHosts:
    - host:
      - docs.staging.jujucharms.com
      tlsSecret: docs-staging-jujucharms-com-tls
```

### noTls
Type: Boolean

```
- host:
  - ubuntu.net
  noTls: true
```

## nginxConfig
Type: String
```
nginxConfig:  |
  if ($host != 'canonical.com' ) {
    rewrite ^ https://canonical.com$request_uri? permanent;
  }
  more_set_headers "Link: <https://assets.ubuntu.com>; rel=preconnect; crossorigin, <https://assets.ubuntu.com>; rel=preconnect";
```

## production
Under this level you can overwrite any of the above mentioned properties for this environment.

## staging
Under this level you can overwrite any of the above mentioned properties for this environment.
