#!/bin/sh
curl http://0pointer.de/lennart/projects/libcanberra/ 2>/dev/null |grep 'current release is' |sed -e 's,</a>.*,,;s,.*>,,'
