import cherrypy, search, json

class searchService(object):
	exposed = True
	
	@cherrypy.tools.accept(media="text/plain")
	def POST(self, query, page):
		res = search.query(query, page)
		res = json.dumps(res)
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'	
	
		return res

if __name__ == '__main__':
	conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True,
			'tools.response_headers.on': True,
			'tools.response_headers.headers': [('Content-Type', 'text/plain')],
		}
	}

	cherrypy.config.update({'server.socket_host': '0.0.0.0'})
	cherrypy.quickstart(searchService(), '/', conf)
