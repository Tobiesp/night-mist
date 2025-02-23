import argparse


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DATABASE_URL = ""
    ADMIN_INITIAL_PASSWORD = 'Adm1n#U$3r'


def parse():
    parser = argparse.ArgumentParser(prog='score-keeper')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode', env_var='DEBUG')
    parser.add_argument('--testing', action='store_true', help='Enable testing mode', env_var='TESTING')
    parser.add_argument('--secret-key', type=str, help='Secret key', env_var='SECRET_KEY')
    parser.add_argument('--csrf-enabled', action='store_true', help='Enable CSRF', env_var='CSRF_ENABLED')
    parser.add_argument('--database-url', type=str, required=True, help='Connection Database URL', env_var='DATABASE_URL')
    parser.add_argument('--admin-initial-password', type=str, help='Admin initial password', env_var='ADMIN_INITIAL_PASSWORD')
    args = parser.parse_args()
    config = Config()
    config.DATABASE_URL = args.database_url
    config.DEBUG = args.debug
    config.TESTING = args.testing
    config.CSRF_ENABLED = args.csrf_enabled
    config.SECRET_KEY = args.secret_key
    config.ADMIN_INITIAL_PASSWORD = args.admin_initial_password
    return config