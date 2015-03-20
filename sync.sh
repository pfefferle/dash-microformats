#!/bin/sh

httrack http://microformats.org/wiki/profile-uris http://microformats.org/profile/specs/ http://gmpg.org/xfn/11 \
  -O Microformats.docset/Contents/Resources/Documents,cache -I0 \
  --display=2 --timeout=60 --retries=99 --sockets=7 \
  --connection-per-second=5 --max-rate=250000 \
  --keep-alive --depth=2 --mirror --clean --robots=0 \
  --user-agent '$(httrack --version); dash-microformats ()' \
  "-*" "-microformats.org/wiki/*" "-gmpg.org/xfn/*" \
  "+microformats.org/profile/*"
