from flask import request, abort, redirect

def domain_based_routing(app):
    @app.before_request
    def handle_domain():
        host = request.host.split(':')[0]  # Remove port if present
        if not host == 'skaffa.net' and not host == 'www.skaffa.net':
            return redirect('https://bing.com/')