import os


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'JMJbGAxb1zVAdWkgPm03JBen'
    PG_CONFIG = {
        'username': 'root',
        'password': 'test',
        'host': os.environ.get('POSTGRES_HOST') or 'db',
        'port': 3306,
        'dbname': os.environ.get('POSTGRES_DB') or 'customer'
    }
