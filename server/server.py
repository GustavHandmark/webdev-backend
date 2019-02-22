import bottle
import queries

def main():
    app = application = bottle.default_app()
    bottle.run(host = "localhost", port = 7007,debug=True)

if __name__ == '__main__':
    main()