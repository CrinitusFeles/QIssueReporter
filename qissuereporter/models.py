from datetime import UTC, datetime
from typing import Any
from pydantic import BaseModel, Field


class BugReportModel(BaseModel):
    username: str = ''
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat(" ", 'seconds'))
    client_version: str
    report_type: str
    title: str
    version: str
    details: str
    images: list[str]
    images_size: float

    def query(self) -> dict[str, str]:
        report_type: dict[str, str] = {
            'Bug Report': 'Bug',
            'Feature Request': 'Feature',
            'Performance Issue (freeze, slow, crash)': 'Task'
        }
        images: str = '\n'.join([f'<img src=\"data:image/jpeg;base64,{image}\"'\
                                 f' alt=\"image_{i}\"/>'
                                 for i, image in enumerate(self.images)])
        content: str = self.details + f'\n{images}' if len(images) > 1 else self.details
        body: dict[str, str] = {
            'title': self.title,
            'type': report_type.get(self.report_type, 'Bug'),
            'body': content,
        }
        return body


class IssueBase(BaseModel):
    id: int # 208045946,
    node_id: str # "MDU6TGFiZWwyMDgwNDU5NDY=",
    url: str # "https://api.github.com/repos/octocat/Hello-World/labels/bug",
    description: str | None = None # "Something isn't working",
    html_url: str | None = None # "https://github.com/octocat",


class IssueContentModel(BaseModel):
    title: str
    url: str
    number: int
    is_opened: bool
    content: str
    images: list[str] = Field(default_factory=lambda:[])
    created_at: str
    issue_type: str
    closed_at: str | None = None
    close_reason: str | None = None


class LabelModel(IssueBase):
    name: str # "bug",
    color: str # "f29513",
    default: bool # true


class UserModel(IssueBase):
    login: str | None = None# "octocat",
    avatar_url: str | None = None # "https://github.com/images/error/octocat_happy.gif",
    gravatar_id: str | None = None # "",
    followers_url: str | None = None # "https://api.github.com/users/octocat/followers",
    following_url: str | None = None # "https://api.github.com/users/octocat/following{/other_user}",
    gists_url: str | None = None # "https://api.github.com/users/octocat/gists{/gist_id}",
    starred_url: str | None = None # "https://api.github.com/users/octocat/starred{/owner}{/repo}",
    subscriptions_url: str | None = None # "https://api.github.com/users/octocat/subscriptions",
    organizations_url: str | None = None # "https://api.github.com/users/octocat/orgs",
    repos_url: str | None = None# "https://api.github.com/users/octocat/repos",
    events_url: str | None = None # "https://api.github.com/users/octocat/events{/privacy}",
    received_events_url: Any | None = None# "https://api.github.com/users/octocat/received_events",
    type: Any # "User",
    site_admin: Any | None = None # false


class MilestoneModel(IssueBase):
    labels_url: str | None = None  # "https://api.github.com/repos/octocat/Hello-World/milestones/1/labels",
    number: int | None = None # 1,
    state: str  # "open",
    title: str  # "v1.0",
    creator: UserModel | None= None
    open_issues: int | None = None # 4,
    closed_issues: int | None = None # 8,
    created_at: str | None = None # "2011-04-10T20:09:31Z",
    updated_at: str| None = None  # "2014-03-03T18:58:10Z",
    closed_at: str | None = None  # "2013-02-12T13:22:01Z",
    due_on: str | None = None  # "2012-10-09T23:39:01Z"


class RepositoryModel(BaseModel):
      id: int  # 1296269,
      node_id: str  # "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
      name: str  # "Hello-World",
      full_name: str  # "octocat/Hello-World",
      owner: UserModel  # {
      private: bool  # false,
      html_url: str  # "https://github.com/octocat/Hello-World",
      description: str  # "This your first repo!",
      fork: bool  # false,
      url: str  # "https://api.github.com/repos/octocat/Hello-World",
      archive_url: str  # "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
      assignees_url: str  # "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
      blobs_url: str  # "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
      branches_url: str  # "https://api.github.com/repos/octocat/Hello-World/branches{/branch}",
      collaborators_url: str  # "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
      comments_url: str  # "https://api.github.com/repos/octocat/Hello-World/comments{/number}",
      commits_url: str  # "https://api.github.com/repos/octocat/Hello-World/commits{/sha}",
      compare_url: str  # "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
      contents_url: str  # "https://api.github.com/repos/octocat/Hello-World/contents/{+path}",
      contributors_url: str  # "https://api.github.com/repos/octocat/Hello-World/contributors",
      deployments_url: str  # "https://api.github.com/repos/octocat/Hello-World/deployments",
      downloads_url: str  # "https://api.github.com/repos/octocat/Hello-World/downloads",
      events_url: str  # "https://api.github.com/repos/octocat/Hello-World/events",
      forks_url: str  # "https://api.github.com/repos/octocat/Hello-World/forks",
      git_commits_url: str  # "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
      git_refs_url: str  # "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
      git_tags_url: str  # "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
      git_url: str  # "git:github.com/octocat/Hello-World.git",
      issue_comment_url: str  # "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
      issue_events_url: str  # "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
      issues_url: str  # "https://api.github.com/repos/octocat/Hello-World/issues{/number}",
      keys_url: str  # "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
      labels_url: str  # "https://api.github.com/repos/octocat/Hello-World/labels{/name}",
      languages_url: str  # "https://api.github.com/repos/octocat/Hello-World/languages",
      merges_url: str  # "https://api.github.com/repos/octocat/Hello-World/merges",
      milestones_url: str  # "https://api.github.com/repos/octocat/Hello-World/milestones{/number}",
      notifications_url: str  # "https://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}",
      pulls_url: str  # "https://api.github.com/repos/octocat/Hello-World/pulls{/number}",
      releases_url: str  # "https://api.github.com/repos/octocat/Hello-World/releases{/id}",
      ssh_url: str  # "git@github.com:octocat/Hello-World.git",
      stargazers_url: str  # "https://api.github.com/repos/octocat/Hello-World/stargazers",
      statuses_url: str  # "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
      subscribers_url: str  # "https://api.github.com/repos/octocat/Hello-World/subscribers",
      subscription_url: str  # "https://api.github.com/repos/octocat/Hello-World/subscription",
      tags_url: str  # "https://api.github.com/repos/octocat/Hello-World/tags",
      teams_url: str  # "https://api.github.com/repos/octocat/Hello-World/teams",
      trees_url: str  # "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
      clone_url: str  # "https://github.com/octocat/Hello-World.git",
      mirror_url: str  # "git:git.example.com/octocat/Hello-World",
      hooks_url: str  # "https://api.github.com/repos/octocat/Hello-World/hooks",
      svn_url: str  # "https://svn.github.com/octocat/Hello-World",
      homepage: str  # "https://github.com",
      language: Any  # null,
      forks_count: int  # 9,
      stargazers_count: int  # 80,
      watchers_count: int  # 80,
      size: int  # 108,
      default_branch: str  # "master",
      open_issues_count: int  # 0,
      is_template: bool  # true,
      topics: list[str] = []
      has_issues: bool  # true,
      has_projects: bool  # true,
      has_wiki: bool  # true,
      has_pages: bool  # false,
      has_downloads: bool  # true,
      archived: bool  # false,
      disabled: bool  # false,
      visibility: str  # "public",
      pushed_at: str  # "2011-01-26T19:06:43Z",
      created_at: str  # "2011-01-26T19:01:12Z",
      updated_at: str  # "2011-01-26T19:14:43Z",
      permissions: dict[str, bool] = {}
      allow_rebase_merge: bool  # true,
      template_repository: Any  # null,
      temp_clone_token: str  # "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
      allow_squash_merge: bool  # true,
      allow_auto_merge: bool  # false,
      delete_branch_on_merge: bool  # true,
      allow_merge_commit: bool  # true,
      subscribers_count: int  # 42,
      network_count: int  # 0,
      license: dict
      forks: int  # 1,
      open_issues: int  # 1,
      watchers: int  # 1


class ResponseModel(UserModel, MilestoneModel):
    repository_url: str # "https://api.github.com/repos/octocat/Hello-World",
    comments_url: str # "https://api.github.com/repos/octocat/Hello-World/issues/1347/comments",
    state: str # "open",
    title: str # "Found a bug",
    body: str # "I'm having a problem with this.",
    user: UserModel# {
    node_id: str # "MDQ6VXNlcjE=",
    avatar_url: str | None = None # "https://github.com/images/error/octocat_happy.gif",
    gravatar_id: str | None = None# "",
    labels: list[LabelModel] = []
    assignee: UserModel | None = None
    assignees: list[UserModel] = []
    milestone: MilestoneModel | None = None
    pull_request: dict = {}
    locked: bool  # true,
    active_lock_reason: str | None  # "too heated",
    comments: int  # 0,
    repository: RepositoryModel | None = None
    author_association: str  # "COLLABORATOR"
