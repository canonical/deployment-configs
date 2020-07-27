# Canonical Web Team Kubernetes configs

This repository contains our ConfigMaps for Kubernetes and our CronJobs configurations; these cronjobs are applied using the [Konf snap](https://github.com/canonical-web-and-design/konf).

## Files

- `configmaps`: In this folder, you will find all the ConfigMap objects that we apply to our cluster.
- `cronjobs`: In this folder, you will find all the CronJob objects that we execute periodically.

## Deploying

To deploy any changes in the current configuration files, update the branch master of this repo by opening a PR with the changes that you want to make.

If you want to add a new ConfigMap or CronJob, create a new yaml file with the configuration and make sure that the Jenkins job is also updated.

**If you are looking for our website configuration files, we have moved these files into each website repo, you could find them under the `konf` folder in each website. [Here](https://github.com/canonical-web-and-design/ubuntu.com/tree/master/konf) is the one for ubuntu.com. To apply these configurations take a look into the [Konf snap repo](https://github.com/canonical-web-and-design/konf)**
