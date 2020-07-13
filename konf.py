#!/usr/bin/env python3

import argparse
import os

import jinja2
import yaml


BASE_DIR = os.getenv("SNAP", ".")
TEMPLATES_DIR = BASE_DIR + "/templates"


# Custom Jinja2 functions
@jinja2.contextfunction
def get_site_name(context, add_staging_prefix=False):
    """Return the metadata name to use for the K8s objects."""
    domain = context["domain"].split(".")

    if add_staging_prefix and context["deployment_env"] == "staging":
        # Return the staging name if there is one specified
        if "name" in context["data"].get("staging", {}):
            return context["data"]["staging"]["name"]
        else:
            domain.insert(-2, "staging")
    elif context["name"]:
        # Return the production name if there is one specified
        return context["name"]

    return "-".join(domain)


@jinja2.contextfunction
def get_environment_domain(context):
    """Return the environment domain."""
    domain = context["domain"]

    if context["deployment_env"] == "staging":
        # Return the staging domain if there is one specified
        if "domain" in context["data"].get("staging", {}):
            domain = context["data"]["staging"]["domain"]
        else:
            domain = add_environment_prefix(context, domain)

    return domain


@jinja2.contextfilter
def add_environment_prefix(context, s):
    """Return the domain with the staging prefix if needed."""
    domain = s.split(".")

    if context["deployment_env"] == "staging":
        domain.insert(-2, "staging")

    return ".".join(domain)


@jinja2.contextfilter
def is_apex_domain(context, s):
    """Check if the given string is an apex/base domain"""
    return s.count(".") == 1


class Konf:
    def __init__(
        self, values_file, env, local_qa, docker_tag, database_url, overrides
    ):
        self.deployment_env = env
        self.values_file = values_file
        self.local_qa = local_qa
        self.docker_tag = docker_tag
        self.database_url = database_url
        self.overrides = overrides

        # Load project data
        self.load_values()

        if self.database_url:
            # Replace database URL in main deployment and in routes
            def _replace_database_url(envs, database_url):
                for index, env in enumerate(envs):
                    if "DATABASE_URL" in env["name"]:
                        envs.pop(index)
                        break
                envs.append({"name": "DATABASE_URL", "value": database_url})

            # Replace in top level "env" definition
            _replace_database_url(
                self.values.get("env", []), self.database_url
            )

            # Replace in routes "env" definitions
            if self.deployment_env in self.values:
                routes = self.values[self.deployment_env].get("routes", [])
                for route in routes:
                    _replace_database_url(route.get("env"), self.database_url)

    def load_values(self):
        raise NotImplementedError

    def render(self, template_file):
        """Returns templates rendered."""

        # Init Jinja2 environment
        template_loader = jinja2.FileSystemLoader(TEMPLATES_DIR)
        jinja_env = jinja2.Environment(
            loader=template_loader, undefined=jinja2.StrictUndefined
        )

        # Add custom jinja2 functions and filters
        jinja_env.globals["get_site_name"] = get_site_name
        jinja_env.globals["get_environment_domain"] = get_environment_domain
        jinja_env.filters["add_environment_prefix"] = add_environment_prefix
        jinja_env.filters["is_apex_domain"] = is_apex_domain

        template = jinja_env.get_template(template_file)

        return template.render(
            name=self.name,
            domain=self.domain,
            tag=self.tag,
            data=self.values,
            namespace=self.namespace,
            deployment_env=self.deployment_env,
        )


class KonfCronJob(Konf):
    def load_values(self):
        """This reads the cronjob values from the yaml file

        Parameters:
        values_file (io.TextIOWrapper): project values
        env (string): production or staging
        local_qa (boolean): Override values for local qa
        docker_tag (string): Override docker tag value
        """

        self.values = yaml.load(self.values_file, Loader=yaml.FullLoader)

        for override in self.overrides:
            key, value = override.split("=")
            self.values[key] = value

        self.name = self.values.get("name")
        self.domain = None

        # Set deployment environment namespace
        self.namespace = self.deployment_env

        # QA overrides
        if self.local_qa:
            self.namespace = "default"

        if self.docker_tag:
            self.tag = self.docker_tag

    def render(self, template_file="cronjob.yaml"):
        return super(KonfCronJob, self).render(template_file)


class KonfSite(Konf):
    def load_values(self):
        """This reads the project values from the yaml file

        Parameters:
        values_file (io.TextIOWrapper): project values
        env (string): production or staging
        local_qa (boolean): Override values for local qa
        docker_tag (string): Override docker tag value
        """

        self.values = yaml.load(self.values_file, Loader=yaml.FullLoader)

        for override in self.overrides:
            key, value = override.split("=")
            self.values[key] = value

        self.name = self.values.get("name")
        self.domain = self.values["domain"]

        # Environment overrides
        self.values.update(self.values.get(self.deployment_env, {}))

        # Set deployment environment namespace
        self.namespace = self.deployment_env

        # QA overrides
        if self.local_qa or self.deployment_env == "demo":
            self.namespace = "default"
            self.values["replicas"] = 1

            for route in self.values.get("routes", []):
                route.update({"replicas": 1})

        if self.docker_tag:
            self.tag = self.docker_tag

    def render(self, template_file="site.yaml"):
        return super(KonfSite, self).render(template_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Render kubernetes configurations for each projects"
    )

    parser.add_argument(
        "--type",
        type=str,
        help="Type of deployment configuration to generate",
        choices=["Site", "CronJob"],
        default="Site",
        dest="konf_type",
    )

    parser.add_argument(
        "--local-qa", action="store_true", default=False, dest="local_qa"
    )

    parser.add_argument(
        "env",
        type=str,
        help="Deployment environment.",
        choices=["production", "staging", "demo"],
    )

    parser.add_argument(
        "values_file",
        type=argparse.FileType("r"),
        help="Project configuration values",
    )

    parser.add_argument(
        "--tag",
        type=str,
        help="Docker tag to deploy",
        default="latest",
        dest="docker_tag",
    )

    parser.add_argument("--database-url", type=str, default=None)

    parser.add_argument(
        "-o", type=str, nargs="+", default=[], dest="overrides",
    )

    args = vars(parser.parse_args())
    konf_type = args.pop("konf_type")
    projectConfig = globals()["Konf" + konf_type](**args)
    print(projectConfig.render())
