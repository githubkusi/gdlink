from setuptools import setup, find_packages

setup(
    name='gdlink-target',
    version='0.1.0',
    description='A script to resolve Google Drive shortcuts and get the target path.',
    author='Markus Leuthold',
    author_email='github@titlis.org',
    url='https://github.com/yourusername/gdlink-target',  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        'google-auth-oauthlib',
        'google-auth',
        'google-api-python-client',
        'argparse',  # argparse is included in the standard library, but can be listed for clarity
    ],
    entry_points={
        'console_scripts': [
            'gdlink=src.gdlink_target:main',  # This allows you to run the script as a command
        ],
    },
    python_requires='>=3.6',  # Specify the Python version required
)