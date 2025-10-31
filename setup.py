"""
Prophet Sentinel - 安装配置
"""
from setuptools import setup, find_packages

setup(
    name="prophet-sentinel",
    version="1.0.0",
    description="AI-powered DeFi Risk Guardian",
    author="Prophet Sentinel Team",
    packages=find_packages(where='backend'),
    package_dir={'': 'backend'},
    python_requires='>=3.8',
    install_requires=[
        'flask>=3.0.0',
        'flask-cors>=4.0.0',
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'scikit-learn>=1.3.0',
        'solana>=0.30.0',
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
        ]
    }
)

