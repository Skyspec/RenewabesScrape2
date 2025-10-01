from .nsw_major_projects import NSWMajorProjects
from .qld_qtenders import QLDQTenders

AVAILABLE_SOURCES = {
    "nsw_major_projects": NSWMajorProjects,
    "qld_qtenders": QLDQTenders,
}
from .icn_gateway import ICNGateway
from .rss_feeds import RSSFeeds

AVAILABLE_SOURCES.update({
    "icn_gateway": ICNGateway,
    "rss_feeds": RSSFeeds,
})
