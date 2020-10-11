import sys
from primer import app
from primer.blueprints.customers import customers
from primer.blueprints.payment_methods import payment_methods

def main(argv):
    app.register_blueprint(customers)
    app.register_blueprint(payment_methods)

    if argv[1] == 'api':
        app.run()
    else:
        print('Sorry no valid option given')
        exit(-1)


if __name__ == '__main__':
    main(sys.argv)

