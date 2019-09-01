from gevent.wsgi import WSGIServer
import sys

from app.app import create_app

environments = {
    'test': 'config.TestingConfig',
    'development': 'config.DevelopmentConfig',
    'production': 'config.ProductionConfig'
}

try:
    if sys.argv[1] in environments.keys():
        app = create_app(environments.get(sys.argv[1]))
        # Run the app
        http_server = WSGIServer(('', 5004), app)
        http_server.serve_forever()

    else:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print ('Usage: python run.py <environment>')
            print ('\n Available options')
            print ('\t -- production \n\t -- development \n\t -- test')
except IndexError:
    # Handle missing arguments or more unfriendly options than required
    print ("Missing options: use [python run.py -h] \
         to get list of available options")
exit()