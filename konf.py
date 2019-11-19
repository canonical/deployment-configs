#! /usr/bin/env python3

import yaml
import jinja2
import argparse


# Custom Jinja2 functions
@jinja2.contextfunction
def get_site_name(context, add_staging_prefix=False):
    """Return the metadata name to use for the K8s objects."""
    if context["data"].get("name"):
        name = context["data"].get("name")
    else:
        domain = context["domain"].split(".")

        if add_staging_prefix and context["deployment_env"] == "staging":
            domain.insert(-2, "staging")

        name = "-".join(domain)

    return name


@jinja2.contextfilter
def get_environment_domain(context, s):
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
    def __init__(self, values_file, env, local_qa=False, docker_tag=None):
        self.deployment_env = env

        # Load project data
        self.load_values(values_file, local_qa, docker_tag)

    def load_values(self, values_file, local_qa=False, docker_tag=None):
        """This reads the project values from the yaml file

        Parameters:
        values_file (io.TextIOWrapper): project values
        env (string): production or staging
        local_qa (boolean): Override values for local qa
        docker_tag (string): Override docker tag value
        """

        self.values = yaml.load(values_file, Loader=yaml.FullLoader)

        self.name = self.values.get("name")
        self.domain = self.values["domain"]

        # Environment overrides
        self.values.update(self.values.get(self.deployment_env, {}))

        # Set deployment environment namespace
        self.values["namespace"] = self.deployment_env

        # QA overrides
        if local_qa:
            qa_values = yaml.load(
                open("qa-overrides.yaml"), Loader=yaml.FullLoader
            )
            self.values.update(qa_values[self.deployment_env])

        if docker_tag:
            self.values["tag"] = docker_tag

    def render(self):
        """Returns templates rendered."""

        # Init Jinja2 environment
        template_loader = jinja2.FileSystemLoader("./templates")
        jinja_env = jinja2.Environment(loader=template_loader)

        # Add custom jinja2 functions and filters
        jinja_env.globals["get_site_name"] = get_site_name
        jinja_env.filters["get_environment_domain"] = get_environment_domain
        jinja_env.filters["is_apex_domain"] = is_apex_domain

        template = jinja_env.get_template("site.yaml")

        return template.render(
            name=self.name,
            domain=self.domain,
            data=self.values,
            deployment_env=self.deployment_env,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Render kubernetes configurations for each projects"
    )

    parser.add_argument(
        "--local-qa", action="store_true", default=False, dest="local_qa"
    )

    parser.add_argument(
        "env",
        type=str,
        help="Deployment environment.",
        choices=["production", "staging"],
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

    args = parser.parse_args()
    projectConfig = Konf(**vars(args))
    print(projectConfig.render())
