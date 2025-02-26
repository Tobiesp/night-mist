import argparse
import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DATABASE_URL = ""
    ADMIN_INITIAL_PASSWORD = 'Adm1n#U$3r'
    PORT = 5000
    HOST = 'localhost'
    SSL = False
    EMAIL_FROM = ''
    EMAIL_SERVER = ''
    EMAIL_PORT = 465
    EMAIL_USERNAME = ''
    EMAIL_PASSWORD = ''


def parse():
    parser = argparse.ArgumentParser(prog='score-keeper')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode', default=False)
    parser.add_argument('--testing', action='store_true', help='Enable testing mode', default=False)
    parser.add_argument('--secret-key', type=str, help='Secret key')
    parser.add_argument('--csrf-enabled', action='store_true', help='Enable CSRF', default=False)
    parser.add_argument('--database-url', type=str, required=True, help='Connection Database URL')
    parser.add_argument('--admin-initial-password', type=str, help='Admin initial password')
    parser.add_argument('--port', type=int, help='Port to run the application')
    parser.add_argument('--host', type=str, help='Host to run the application')
    parser.add_argument('--ssl', action='store_true', help='Use SSL', default=False)
    parser.add_argument('--email-from', type=str, help='Email from')
    parser.add_argument('--email-server', type=str, help='Email server')
    parser.add_argument('--email-port', type=int, help='Email port')
    parser.add_argument('--email-username', type=str, help='Email username')
    parser.add_argument('--email-password', type=str, help='Email password')
    args = parser.parse_args()
    config = Config()
    config.DATABASE_URL = args.database_url or os.environ.get('DATABASE_URL')
    if config.DATABASE_URL is None:
        raise ValueError('Database URL is required')
    config.DEBUG = args.debug or bool(os.environ.get('DEBUG'))
    config.TESTING = args.testing or bool(os.environ.get('TESTING'))
    config.CSRF_ENABLED = args.csrf_enabled or bool(os.environ.get('CSRF_ENABLED'))
    config.SECRET_KEY = args.secret_key or os.environ.get('SECRET_KEY')
    if config.SECRET_KEY is None:
        config.SECRET_KEY = 'this-really-needs-to-be-changed'
    config.ADMIN_INITIAL_PASSWORD = (args.admin_initial_password or os.environ.get('ADMIN_INITIAL_PASSWORD'))
    if config.ADMIN_INITIAL_PASSWORD is None:
        config.ADMIN_INITIAL_PASSWORD = 'Adm1n#U$3r'
    config.PORT = args.port or os.environ.get('PORT')
    if config.PORT is None:
        config.PORT = 5000
    config.HOST = args.host or os.environ.get('HOST')
    if config.HOST is None:
        config.HOST = 'localhost'
    config.SSL = args.ssl or bool(os.environ.get('SSL'))
    config.EMAIL_FROM = args.email_from or os.environ.get('EMAIL_FROM')
    config.EMAIL_SERVER = args.email_server or os.environ.get('EMAIL_SERVER')
    config.EMAIL_PORT = args.email_port or os.environ.get('EMAIL_PORT')
    config.EMAIL_USERNAME = args.email_username or os.environ.get('EMAIL_USERNAME')
    config.EMAIL_PASSWORD = args.email_password or os.environ.get('EMAIL_PASSWORD')
    return config