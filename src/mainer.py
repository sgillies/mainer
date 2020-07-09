"""Help repo users move from master to main"""

from difflib import unified_diff
import itertools
import logging
import os
import pathlib
import re

import click
import github
import structlog
from structlog.stdlib import LoggerFactory

__version__ = "1.0dev"

log = structlog.get_logger(__name__)


@click.command()
@click.argument("repo", metavar="ORG/REPO")
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Print comment diffs to stderr, but make no edits.",
)
@click.option(
    "--rewrite-links-to",
    "linked_repo",
    default=None,
    help="The repo named in the links to be fixed. For example: 'org2/repo2'. Defaults to ORG/REPO.",
)
@click.option(
    "--access-token",
    default=None,
    help="A GitHub access token. May also be set by GITHUB_ACCESS_TOKEN or GithubAccessToken in the environment.",
)
def main(repo, dry_run, linked_repo, access_token):
    """Rewrite links in a repo's issue and PR comments so that they point to the linked repo's main branch instead of its master branch.

    Example:

    python -m mainer org1/repo1 --rewrite-links-to org2/repo2 --dry-run

    """
    if access_token is None:
        access_token = os.getenv("GITHUB_ACCESS_TOKEN") or os.getenv(
            "GithubAccessToken"
        )
    if linked_repo is None:
        linked_repo = repo

    g = github.Github(access_token)
    repo = g.get_repo(repo)

    pattern = re.compile(rf"{linked_repo}/(\w+)/master")

    for item in itertools.chain(
        repo.get_issues(), repo.get_issues_comments(), repo.get_pulls(), repo.get_pulls_comments()
    ):
        match = re.search(pattern, item.body)
        if match:

            def repl(match):
                return f"{linked_repo}/{match.group(1)}/main"

            modified_body = re.sub(pattern, repl, item.body)
            diff = unified_diff(
                item.body.splitlines(True), modified_body.splitlines(True)
            )
            url = "/".join(pathlib.Path(item.url).parts[-4:])

            if dry_run:
                click.echo(f"\nChanges for {url}", err=True)
                for line in diff:
                    click.echo(line, nl=False, err=True)
            else:
                log.info(
                    "Editing item",
                    item=item,
                    url=url,
                    diff=list(line for line in diff),
                )
                if isinstance(item, (github.Issue.Issue, github.PullRequest.PullRequest)):
                    item.edit(body=modified_body)
                else:
                    item.edit(modified_body)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    structlog.configure(logger_factory=LoggerFactory())
    main()
