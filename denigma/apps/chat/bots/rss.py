try:
    from feedparser import parse
except ImportError:
    parse = None

from denigma.apps.chat.bots import events


class RSSMixin(object):
    """Mixin for bots that consume RSS feeds and post them to the channel.
    Feeds are defined by the ``feeds`` keywords arg to ``__init__`, adn should
    contain a sequence of RSS feed URLs.

    Requires the ``feedparser`` library to be installed."""
    def __init__(self, *args, **kwargs):
        if parse is None:
            from warnings import warn
            warn("RSSMixin requires feedparser installed")
        self.feeds = kwargs.pop('feeds', [])
        self.feed_items = set()
        # Consume initial feed items without posting them.
        self.parse_feeds(message_channel=False)
        super(RSSMixin, self).__init__(*args, **kwargs)

    @events.on('timer', seconds=60)
    def parse_feeds(self, message_channel=True):
        """Iterates through each of the feed URLs, parses their items, and
        sends any items to the channel that have not been previously
        been parsed."""
        if parse:
            for feed in self.feeds:
                for item in parse(feed).entries:
                    if item['id'] not in self.feed_items:
                        self.feed_items.add(item['id'])
                        if message_channel:
                            self.message_channel('%(title)s: %(id)s' % item)
                            return
