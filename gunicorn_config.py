# gunicorn_config.py

bind = '127.0.0.1:5001'  # Bind to all available network interfaces
workers = 1  # Adjust the number of workers based on your server resources
# more the number of worker nodes, more number of times model will get initialised
timeout = 250  # Maximum request processing time (in seconds)
# worker_class = 'gthread'  # or 'gthread'


# loglevel = 'debug'  # Adjust the logging level (debug, info, warning, error)
accesslog = '-'  # Log access information to the console (or specify a file)
errorlog = '-'  # Log errors to the console (or specify a file)

wsgi_app = 'privateGPT:app'  # Specify the Flask app entry point
