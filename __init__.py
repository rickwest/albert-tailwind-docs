# -*- coding: utf-8 -*-

"""Search the Tailwind CSS Documentation"""

from os import path
import urllib.parse
import html
from algoliasearch.search_client import SearchClient

from albertv0 import *

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "Tailwind CSS Docs"
__version__ = "0.1.0"
__trigger__ = "tw "
__author__ = "Rick West"
__dependencies__ = ["algoliasearch"]


client = SearchClient.create("BH4D9OD16A", "3df93446658cd9c4e314d4c02a052188")
index = client.init_index("tailwindcss")


icon = "{}/icon.jpg".format(path.dirname(__file__))
google_icon = "{}/google.png".format(path.dirname(__file__))


def getSubtitles(hit):
    hierarchy = hit["hierarchy"]

    subtitles = []
    for x in range(2, 6):
        if hierarchy["lvl" + str(x)] is not None:
            subtitles.append(hierarchy["lvl" + str(x)])

    return subtitles


def sortByLevel(el):
    return el["hierarchy"]["lvl0"]


def handleQuery(query):
    items = []

    if query.isTriggered:

        if not query.isValid:
            return

        if query.string.strip():
            search = index.search(query.string, {"hitsPerPage": 5})

            hits = search["hits"]

            if len(hits) is not 0:
                hits.sort(key=sortByLevel)

            for hit in hits:

                if len(getSubtitles(hit)) is not 0:
                    subtitle = "[{}] - {}".format(
                        hit["hierarchy"]["lvl0"], " » ".join(getSubtitles(hit))
                    )
                else:
                    subtitle = "[{}]".format(hit["hierarchy"]["lvl0"])

                items.append(

                    Item(
                        id=__prettyname__,
                        icon=icon,
                        text=html.unescape(hit["hierarchy"]["lvl1"]),
                        subtext=html.unescape(subtitle),
                        actions=[
                            UrlAction("Open in the Tailwind CSS Documentation", hit["url"])
                        ],
                    )
                )

            if len(items) == 0:
                term = "tailwind css {}".format(query.string)

                google = "https://www.google.com/search?q={}".format(
                    urllib.parse.quote(term)
                )

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=google_icon,
                        text="Search Google",
                        subtext='No match found. Search Google for: "{}"'.format(term),
                        actions=[UrlAction("No match found. Search Google", google)],
                    )
                )

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=icon,
                        text="Open Docs",
                        subtext="No match found. Open tailwindcss.com/docs...",
                        actions=[
                            UrlAction(
                                "Open the Tailwind CSS Documentation",
                                "https://tailwindcss.com/docs",
                            )
                        ],
                    )
                )

        else:
            items.append(
                Item(
                    id=__prettyname__,
                    icon=icon,
                    text="Open Docs",
                    subtext="Open tailwindcss.com/docs...",
                    actions=[
                        UrlAction(
                            "Open the Tailwind CSS Documentation", "https://tailwindcss.com/docs"
                        )
                    ],
                )
            )

    return items
