mainer
======

Mainer helps GitHub repo users switch "master" branches to "main".

Branch renaming is the easy part. But you may be left with hundreds or
thousands of links to "master" in GitHub issue and PR comments. This is where
mainer comes in.

# Usage

```
$ python -m mainer --help
Usage: mainer.py [OPTIONS] ORG/REPO

  Rewrite links in a repo's issue and PR comments so that they point to the
  linked repo's main branch instead of its master branch.

  Example:

  python -m mainer org1/repo1 --rewrite-links-to org2/repo2 --dry-run

Options:
  --dry-run                Print comment diffs to stderr, but make no edits.
  --rewrite-links-to TEXT  The repo named in the links to be fixed. For
                           example: 'org2/repo2'. Defaults to ORG/REPO.

  --access-token TEXT      A GitHub access token. May also be set by
                           GITHUB_ACCESS_TOKEN or GithubAccessToken in the
                           environment.

  --help                   Show this message and exit.
```
