from setuptools import setup

setup(
    name            = 'pyxing',
    version         = '0.0.5',
    description     = 'python wrapper for eBest Xing API',
    url             = 'https://github.com/sharebook-kr/pyxing',
    author          = 'Lukas Yoo, Brayden Jo',
    author_email    = 'jonghun.yoo@outlook.com, brayden.jo@outlook.com, pystock@outlook.com',
    install_requires= ['pandas'],
    license         = 'MIT',
    packages        = ['pyxing'],
    zip_safe        = False
)