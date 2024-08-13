from setuptools import setup, find_packages

setup(
    name='amelia_swim',
    packages=find_packages(['./scripts/*']),
    version='1.0',
    url="https://github.com/AmeliaCMU/AmeliaSWIM",
    description='',
    install_requires=[
        'setuptools',
        'tqdm==4.65.0',
        'minio',
        'numpy==1.21.2',
        'pykml',
        'easydict==1.10',
        'pandas==2.0.3',
        'hydra-core==1.3.2',
        'hydra_colorlog==1.2.0',
        'geographiclib==2.0',
        'joblib==1.2.0',
        'shapely==2.0.3',
    ]
)
