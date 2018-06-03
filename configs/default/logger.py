import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'whenAndWhere': {
            'format': '%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s \n%(message)s'
        }
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'whenAndWhere',

        },
    },

    'loggers': {
        'default': {
            'handlers': ['console'],
            'level': 'INFO'
        },
    },
}
