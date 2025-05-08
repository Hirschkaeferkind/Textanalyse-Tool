from setuptools import setup

APP = ['Parser_v2.py']
OPTIONS = {
    'argv_emulation': True,
    'frameworks': [
        '/opt/homebrew/opt/tcl-tk/lib/libtk8.6.dylib',
        '/opt/homebrew/opt/tcl-tk/lib/libtcl8.6.dylib',
    ],
}


setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
