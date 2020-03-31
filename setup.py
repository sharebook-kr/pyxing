from setuptools import setup

setup(
    name            = 'pyxing',
    version         = '0.0.1',
    description     = 'python wrapper for eBest Xing API',
    url             = 'https://github.com/sharebook-kr/pyxing',
    author          = 'Lukas Yoo, Brayden Jo',
    author_email    = 'brayden.jo@outlook.com, jonghun.yoo@outlook.com, pystock@outlook.com',
    install_requires= ['win32com.client', 'pandas', 'pythoncom'],
    license         = 'MIT',
    packages        = ['pyxing'],
    zip_safe        = False
)