from setuptools import setup, find_packages

setup(
    name='XDataExecute',
    version='0.1.4',
    author='LiKaiPeng',
    author_email='Lkpappinventor@outlook.com',
    description='A short description of your library',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SDIJF1521/XDataExecute',  # 如果有GitHub链接
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=['async-timeout==4.0.3',
                      'cffi==1.17.1',
                      'cryptography==43.0.1',
                      'numpy==2.1.2',
                      'pandas==2.2.3',
                      'pycparser==2.22',
                      'PyMySQL==1.1.1',
                      'python-dateutil==2.9.0.post0',
                      'pytz==2024.2',
                      'redis==5.1.1',
                      'six==1.16.0',
                      'tzdata==2024.2',
                      ],
    entry_points={
        'console_scripts': [
            'create-config=common.CreateConfig:main',  # 这里的路径应与您的模块路径相符
        ],
    },
)
