from base import BaseBot
from chat import ChatMixin
from commits import BitBucketMixin, GitHubMixin
from commands import CommandMixin
from rss import RSSMixin


class ChatBox(ChatMixin, BaseBot):
    pass


class BitBucket(BitBucketMixin, BaseBot):
    pass

class GitHubBot(GitHubMixin, BaseBot):
    pass

class CommitBot(GitHubMixin, BitBucketMixin, BaseBot):
    pass

class CommandBot(CommandMixin, BaseBot):
    pass

class RSSBot(RSSMixin, BaseBot):
    pass

class Voltron(ChatMixin,CommandMixin, BitBucketMixin,
        GitHubMixin, RSSMixin, BaseBot):
    pass



