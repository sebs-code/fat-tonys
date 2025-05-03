# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://sebs.website'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# OVERRIDE html content generation
USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'blog'
ARTICLE_SAVE_AS = 'blog-bare/{slug}'
TAG_SAVE_AS = "blog-bare/tag/{slug}"

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""