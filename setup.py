from distutils.core import setup

setup(
    name='Scruffy Video',
    version="0.1",
    author='Jason Goldstein',
    author_email='jason@betheshoe.com',
    url='https://github.com/whatisjasongoldstein/scruffy-video',
    packages=['scruffy_video', ],
    package_data={ 'scruffy_video': ['*',] },
    description='Simple Python utilities for working with video on the web.',
    long_description=open('README.markdown').read(),
)