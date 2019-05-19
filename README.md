# How to adapt this bot for your use

The prerequisites:

```
pip3 install Mastodon.py
pip3 install cairosvg
```

## First, create a bot account and set everything up

The usual stuff. An email address, a password, an avatar, a header,
the bot checkbox, the URL for the application, the account of the
maintainer (you!) and how to reach you. And finally, credentials.

Go to the Mastodon preferences of your new bot account. Under the
"developer" menu there is a place to create a new app and get your
credentials all in one go.

The scopes you need are `write:media` and `write:statuses`.

You need to save the three codes you got as follows:

The *Client key* and *Client secret* go into the first file, each on a
line of its own. The filename is `<account>.client`, for example
`hexdescribe@botsin.space.client`.

Example content:

```
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
```

*Your access token* goes to a separate file called `<account>.user`,
for example `hexdescribe@botsin.space.user`.

Example content:

```
7890abcdef1234567890abcdef1234567890abcdef1234567890abcdef123456
```

## Next, take a look at the code

Here's a simple alternative where we get the image, upload it and, and
post a status for it. You might want to change text and URLs and all
that.

```
text = "#hexdescribe #hex #map #rpg"
png = cairosvg.svg2png(url="https://campaignwiki.org/text-mapper/alpine/random")
media = mastodon.media_post(png, mime_type="image/png", description="a hex map")
mastodon.status_post(text, media_ids=[media.id])
```

If you want to change anything, it's probably going to be here.

## Finally, invoke it

This is what I do:

```
./bot.py hexdescribe@botsin.space
```
