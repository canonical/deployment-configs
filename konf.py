#! /usr/bin/env python3

import yaml
import jinja2
import argparse


# Custom Jinja2 functions
@jinja2.contextfunction
def getSiteName(context, addStaginPrefix=False):
    if context['data'].get('name'):
        name = context['data'].get('name')
    else:
        domain = context['domain'].split(".")

        if addStaginPrefix and context["deploymentEnv"] == "staging":
            domain.insert(-2, 'staging')

        name = "-".join(domain)

    return name


@jinja2.contextfilter
def siteDomain(context, s):
    domain = s.split(".")

    if context["deploymentEnv"] == "staging":
        domain.insert(-2, 'staging')

    return ".".join(domain)


@jinja2.contextfilter
def isApexDomain(context, s):
    return s.count('.') == 1


class Konf:
    def __init__(
        self,
        values_file,
        env,
        local_qa=False,
        docker_tag=None
    ):
        self.deploymentEnv = env

        # Init Jinja2 environment
        templateLoader = jinja2.FileSystemLoader("./templates")
        self.tplEnv = jinja2.Environment(loader=templateLoader)

        # Add custom jinja2 functions and filters
        self.tplEnv.globals['getSiteName'] = getSiteName
        self.tplEnv.filters['siteDomain'] = siteDomain
        self.tplEnv.filters['isApexDomain'] = isApexDomain

        # Load project datadocker_tag
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
        self.values.update(self.values.get(self.deploymentEnv, {}))

        # Set deployment environment namespace
        self.values["namespace"] = self.deploymentEnv

        # QA overrides
        if local_qa:
            qa_values = yaml.load(
                open("qa-overrides.yaml"), Loader=yaml.FullLoader
            )
            self.values.update(qa_values[self.deploymentEnv])

        if docker_tag:
            self.values["tag"] = docker_tag

    def render(self):
        """Returns templates rendered."""
        output = ""

        template = self.tplEnv.get_template("site.yaml")
        output += template.render(
            name=self.name,
            domain=self.domain,
            data=self.values,
            deploymentEnv=self.deploymentEnv,
        )

        return output


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
        dest="docker_tag"
    )

    args = parser.parse_args()
    projectConfig = Konf(**vars(args))
    print(projectConfig.render())
