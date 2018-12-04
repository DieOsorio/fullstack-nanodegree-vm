from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
# Import CRUD Operations
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += "<html><body>"
                names = []
                for restaurant in restaurants:
                    names.append(restaurant.name)
                for name in list(set(names)):
                    output += name
                    output += '</br>'
                    output += "<a href='#'>Edit</a>"
                    output += '</br>'
                    output += "<a href='#'>Delete</a>"
                    output += '</br>'
                    output += '</br>'
                output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += "<html><body>"
                output += 'Hello!'   
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"           
                self.wfile.write(output)
                self.server.path = self.path
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found {}'.format(self.path))

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ''
            output += "<html><body>"
            output += '<h2> Okay, how about this: </h2>'
            output += '<h1>{}</h1>'.format(messagecontent[0])
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output

        except:
            pass


def main():
    try:
        port = 8000
        server = HTTPServer(('', port), WebServerHandler)
        print 'Web server running on port {}'.format(port)
        server.serve_forever()

    except KeyboardInterrupt:
        print '  stopping web server...'
        server.socket.close()

if __name__ == '__main__':
    main()