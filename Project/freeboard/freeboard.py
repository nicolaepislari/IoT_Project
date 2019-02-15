import cherrypy
import json
import os.path
import requests

class freeboard():
    exposed = True

    def GET(self,*uri,**params):

        # The user should user url/(zone name) where zone name could be zone1, zone2...
        # Is this zone is not in the zone list, then we cannot access it
        if len(uri)>=1:
            try:
                file = open("config.json", "r")
                json_str = file.read()
                file.close()
            except:
                raise cherrypy.HTTPError(500,"Error opening config file. Please check.")

            config_json = json.loads(json_str)
            url = config_json["catalog"]["url"]
            respond=requests.get("http://"+url+"/zones")
            respond=respond.json()
            if uri[0] in respond.keys():
                s1 = open("./index.html").read(82).format(test=uri[0])
                s2 = open("./index.html").read()
                s2 = s2[82:]
                s2 = s1 + s2
                return s2
            else:
                raise cherrypy.HTTPError(404,"The link you entered isn't a valid link")
            #return open("./index.html").read()
        else:
            raise cherrypy.HTTPError(404,"Please choose zone.")

    def POST(self,*uri,**params):
        a = params['json_string']
        print a
        txt=open('./dashboard.json','w')
        txt.write(a)
        txt.close()
        return open("./index.html").read()
if __name__ == '__main__':

    path = os.path.abspath(os.path.dirname(__file__))

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())

        },
        '/static':{
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './'
        }
    }

    cherrypy.tree.mount(freeboard(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 7070})
    cherrypy.engine.start()
    cherrypy.engine.block()