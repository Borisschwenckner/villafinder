#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
import time

for subdir, dirs, files in os.walk("/mnt/video/netz/prg/scraper/sicher/"):
    for file in files:
        if not file.startswith(".") :
            path_with_file = subdir + '/' + file
            file_mtime = datetime.fromtimestamp(os.path.getmtime(path_with_file))
            max_mtime = datetime.now() - timedelta(days=10)
            if file_mtime < max_mtime:
                print(path_with_file), file_mtime, max_mtime
                os.remove(path_with_file)
