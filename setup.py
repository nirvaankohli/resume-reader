from setuptools import setup

setup(
    name='resume-reader',
    version='0.1.0',
    py_modules=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'python-dotenv',
        'openai',
        'PyPDF2'
    ],
    entry_points={
        'console_scripts': [
            'run-resume-reader=app:main'
        ]
    },
)
