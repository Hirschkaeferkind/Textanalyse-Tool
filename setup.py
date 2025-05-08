from setuptools import setup

APP = ['Parser_v2.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': [],
    # Entferne "frameworks"
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

