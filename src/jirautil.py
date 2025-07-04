from jira import JIRA
import os
from constants import *

class ClouderaJira(object):
    jira = None

    def __init__(self):

        self._init_jira()

    @classmethod
    def _init_jira(cls):
        if cls.jira:
            return
        username = os.environ.get('JIRA_USERNAME')
        if not username:
            raise Exception(f"JIRA_USERNAME environment variable not set {os.environ}")
        password = os.environ.get('JIRA_TOKEN')
        if not password:
            raise Exception('JIRA_TOKEN environment variable not set')
        jiraOptions = {'server': "https://cloudera.atlassian.net"}
        if not (username and password):
            raise ValueError("Username and/or password is empty")
        cls.jira = JIRA(options=jiraOptions, basic_auth=(username, password))

    def create_releng_promotion_ticket(self, product, build, target_registry):
        rpat_release_config = "public_cloud_stage"
        if target_registry == "Prod":
            rpat_release_config = "public_cloud_prod"

        fields = {
            'project': 'RELENG',
            'issuetype': {
                'name': 'Release'
            },
            'summary': '{prefix_string}Please push {product} {build} images to stage registry'.format(
                prefix_string=PREFIX_STRING,
                product=product,
                build=build),
            "components": [
                {'name': "Releasing"}
            ],
            'description': """
                                We (CML) would like to promote our release to stage and prod asap. We'd like to request to start pushing the docker images.
                                Please push {product} - {build} to stage registry
                            """.format(
                product=product,
                build=build
            ),
            BUILD_IDENTIFIER: build,
            PRODUCT: product,
            RELEASE_TYPE: {'value': target_registry},
            PUBLIC_CLOUD: [{'value': "True"}],
            RPAT_RELEASE_CONFIG: rpat_release_config
        }
        print(fields)
        issue = self.jira.create_issue(fields)
        print("Promotion ticket for {product} is {ticket}".format(product=product, ticket=str(issue)))
        return str(issue)


    def search_jira_issues(self, search_string, project_key=None, max_results=50):
        """
        Search Jira issues by summary string.

        Parameters:
        - search_string (str): The string to search in issue summaries
        - project_key (str, optional): Limit search to a specific project
        - max_results (int): Max number of issues to return

        Returns:
        - List of matching issues (as dicts)
        """

        jql = f'summary ~ "{search_string}"'
        if project_key:
            jql = f'project = {project_key} AND {jql}'

        # Search issues
        issues = self.jira.search_issues(jql, maxResults=max_results)

        # Format output
        return [{
            'key': issue.key,
            'summary': issue.fields.summary,
            'status': issue.fields.status.name,
            'assignee': issue.fields.assignee.displayName if issue.fields.assignee else None,
            'url': f"https://cloudera.atlassian.net/browse/{issue.key}"
        } for issue in issues]

    from jira import JIRA

    def search_jira_issues_by_assignee(
            self,
            assignee_username,
            summary_contains=None,
            project_key=None,
            max_results=50
    ):
        """
        Search Jira issues assigned to a specific user, optionally filtering by summary or project.

        Parameters:
        - assignee_username (str): Username or account ID of the assignee
        - summary_contains (str, optional): Filter issues by summary content
        - project_key (str, optional): Filter by project
        - max_results (int): Max number of results to return

        Returns:
        - List of issues (dicts with key, summary, status, assignee, url)
        """

        # Build JQL query
        jql_parts = [f'assignee = "{assignee_username}"']
        if summary_contains:
            jql_parts.append(f'summary ~ "{summary_contains}"')
        if project_key:
            jql_parts.insert(0, f'project = {project_key}')

        jql = ' AND '.join(jql_parts)

        # Search issues
        issues = self.jira.search_issues(jql, maxResults=max_results)

        return [{
            'key': issue.key,
            'summary': issue.fields.summary,
            'status': issue.fields.status.name,
            'assignee': issue.fields.assignee.displayName if issue.fields.assignee else None,
            'url': f"https://cloudera.atlassian.net/browse/{issue.key}"
        } for issue in issues]


