This deployment can be released file by file but it can also be released in one by pointing kubectl at the parent folder.

`kubectl apply -f .`


The configuration relies on a TLS secret which follows this format:

``` yaml
---
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: design-staging-ubuntu-com-tls
  namespace: default
data:
  tls.crt: dGVzdAo= # Base64 cert
  tls.key: dGVzdAo= # Base64 key
  ca.crt: dGVzdAo= # BAse64 chain (optional)
```
