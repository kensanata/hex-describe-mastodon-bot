#!/usr/bin/env python3
# Copyright (C) 2018–2019  Alex Schroeder <alex@gnu.org>

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from mastodon import Mastodon
import sys
import os.path
import urllib.request
import urllib.parse
import cairosvg
import random
import getopt
import os
import re

def login(account):
    """
    Login to your Mastodon account
    """

    (username, domain) = account.split("@")

    url = 'https://' + domain
    client_secret = account + '.client'
    user_secret = account + '.user'
    mastodon = None

    if not os.path.isfile(client_secret):
        print("Error: you need to create the file '%s'" % client_secret,
              file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(user_secret):
        print("Error: you need to create the file '%s'" % user_secret,
              file=sys.stderr)
        sys.exit(1)

    mastodon = Mastodon(
        client_id = client_secret,
        access_token = user_secret,
        api_base_url = url)

    return mastodon

def main(account, debug=False):
    mastodon = login(account)
    seed = random.randint(0, 2**32)
    svg_url = "https://campaignwiki.org/text-mapper/alpine/random?"
    text_url = "https://campaignwiki.org/text-mapper/alpine/random/text?"
    app_url = "https://campaignwiki.org/hex-describe"
    desc_url = "https://campaignwiki.org/hex-describe/describe/random/alpine?"
    args = ["seed=%d" % seed];
    if random.random() > 0.6:
        args.append("bottom=%d" % random.randint(1,6))
    if random.random() > 0.6:
        args.append("peak=%d" % random.randint(7,9))
    if random.random() > 0.8:
        args.append("peaks=%d" % random.randint(1,20))
    if random.random() > 0.8:
        args.append("steepness=%.1f" % (1 + random.randint(0,50)/10))
    svg_url += "&".join(args)
    text_url += "&".join(args)
    # download SVG
    svg = urllib.request.urlopen(svg_url).read()
    # convert SVG to PNG
    png = cairosvg.svg2png(bytestring=svg)
    # create the status text
    text = ("Here's a new alpine mini-setting for your next hex crawl campaign!\n"
            + desc_url + "url=" + urllib.parse.quote(text_url) + "\n"
            + "Learn about the web app and the tables used to generate it all:\n"
            + app_url + "\n"
            + "#hexdescribe #hex #hexcrawl #map #rpg")
    # abort now if debugging
    if debug:
        print(text)
        sys.exit(0)
    # upload image
    media = mastodon.media_post(png, mime_type="image/png", description="a hex map")
    # post status
    mastodon.status_post(text, media_ids=[media.id])

def usage():
    print("Please provide an account name like nick@example.org")
    print("Use --debug to print the status instead of posting it")
    print("Use --help to print this message")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: you must provide an account", file=sys.stderr)
        sys.exit(1)
    account = sys.argv[1]
    main(account, os.getenv("DEBUG", default=False))
