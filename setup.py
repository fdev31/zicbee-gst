#!/usr/bin/env python
import os
import sys
try:
	import setuptools
except ImportError:
	from ez_setup import use_setuptools
	use_setuptools()
from setuptools import setup, find_packages

sys.path.insert(0, '.')
import zicbee_gst
VERSION=zicbee_gst.__version__

setup (
        name='zicbee-gst',
        version=VERSION,
        author='Fabien Devaux',
        author_email='fdev31@gmail.com',
        url = 'http://zicbee.gnux.info/',
        download_url='http://zicbee.gnux.info/hg/zicbee-gst/archive/%s.tar.bz2'%VERSION,
        license='BSD',
        platform='all',
        description='Gstreamer backend for zicbee project',
        long_description='''Allow zicbee to use gstreamer for playback''',
        keywords = 'database music tags metadata management',
        packages = find_packages(),

        entry_points = """
        [zicbee.player]
        gst = zicbee_gst.core:Player
        """,

        dependency_links = [
            'eggs',
            'http://zicbee.gnux.info/files/',
            'http://webpy.org/',
            'http://buzhug.sourceforge.net/',
            'http://code.google.com/p/quodlibet/downloads/list',
#            'http://sourceforge.net/project/showfiles.php?group_id=167078&package_id=190037&release_id=664931',
#            'http://code.google.com/p/pyglet/downloads/list',
            ],
        classifiers = [
                'Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
#                'Intended Audience :: End Users/Desktop',
                'Operating System :: OS Independent',
                'Operating System :: Microsoft :: Windows',
                'Operating System :: POSIX',
                'Programming Language :: Python',
                'Environment :: Console',
                'Environment :: No Input/Output (Daemon)',
                'Environment :: X11 Applications',
                'Natural Language :: English',
                'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
                'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                'Topic :: Software Development',
                'Topic :: Software Development :: Libraries :: Python Modules',
                'Topic :: Multimedia :: Sound/Audio :: Players',
                'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
                'Topic :: Text Processing :: Markup',
                'Topic :: Utilities',
                ],

        )

