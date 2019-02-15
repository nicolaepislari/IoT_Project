import cherrypy
import json
import requests
import time
import datetime

from classes import *

catalog_name = None


class Catalog_manager():
    '''
        This Class manages the Catalog.
        It exposes a number of WebServices in order to:
        
        1) Retrieve the entire content of the Catalog
        2) Retrieve informaton about a speciffic resource
    '''


    def __init__(self, file):
        '''
            Constructor of Catalog_manager:
            This method initialiaze the attributes 'broker' and 'port' by oppening the catalog.json
            file and takes from it the information about the broker IP-address and the port.
            Arguments:
                file (file): the JSON file containing the content of the catalog 
        '''
        file_conf=open(file,'r')
        self.conf=json.load(file_conf)
        self.broker=self.conf['broker']
        self.port=self.conf['port']
        file_conf.close()

    def print_catalog_WS(self):
        '''
            This WebService returns the content of the "catalog.json" at the current time
            by printing its entire content
        '''
        msg=(
        '''
        Network Settings:
        Broker:   %s 
        Port:     %d
        ''' % (self.conf['broker'],self.conf['port']))
       
        msg = msg + 'Next Settings to be added:'
        return msg





class Catalog_config():
    exposed= True

    def GET(self,*uri,**params):
        if not uri:
            return open(catalog_name)
        if uri[0] == 'print_catalog':
            return Catalog_manager('catalog.json').print_catalog_WS()
        elif uri[0] == 'broker_info':
            catalog = json.load(open('catalog.json', 'r'))
            return json.dumps(catalog['broker'])
        elif uri[0] == 'next_actor':
            print("\n\n%s\n\n" % (params))
            catalog = json.load(open('catalog.json', 'r'))
            actors = catalog['actor']
            print("\n\n%s\n\n" % (actors))
            actors_of_right_type = actors[params["type"]]
            for actor in actors_of_right_type:
                if actor[params['type']+'ID'] == params['ID']:
                    payload = {'status': 'success', 'requirements': actor['requirements']}
                    print (payload)
                    return json.dumps(payload)
            return json.dumps({'status': 'failure'})


    def POST(self,*uri,**params):
        '''
            The method is used to update the information in the catalog.json file
        '''
        # reads the BODY content of the POST Method
        body_payload = cherrypy.request.body.read()
        print ("body_payload = %s" %body_payload)
        print ("type = %s" %type(body_payload.decode("utf-8") ))
        new_data_dict = json.loads(body_payload.decode("utf-8") )

        old_catalog = open(catalog_name, 'r').read()
        old_catalog_dict = json.loads(old_catalog)


        if not uri:
            # reads the BODY content of the POST Method
            body_payload = cherrypy.request.body.read()
            print ("body_payload = %s" %body_payload)
      


        elif uri[0] == "iamalive":
            '''
                check the actors in the catalog file and register/update them 
                with the current time and date
            '''
        
            actor_dict = old_catalog_dict['actor']
            print ("actor dict datatype:  %s" %type(actor_dict))
            print ("new_data datatype: %s" %type(new_data_dict))
            print ("======================================")
            updated_actors, message = Catalog_checker().check_actor(actor_dict, new_data_dict)

    
            old_catalog_dict['actor'] = updated_actors

            catalog_file = open(catalog_name,'w')
            catalog_file.write(json.dumps(old_catalog_dict, indent=4))
            catalog_file.close()

            return message

        elif uri[0] == "removeme":
            actor_dict = old_catalog_dict['actor']
            alive_actors, removed_actors = Catalog_checker().remove_old(actor_dict, 60)
            

            old_catalog_dict['actor'] = alive_actors
            catalog_file = open(catalog_name,'w')
            catalog_file.write(json.dumps(old_catalog_dict, indent=4))
            catalog_file.close()



if __name__ == '__main__':

    file_conf=open('conf.json','r')
    catalog_conf=json.load(file_conf)
    catalog_name=catalog_conf['catalog']
    time_to_live=catalog_conf['time_to_live']
    host = catalog_conf['host']
    port = catalog_conf['port']
    file_conf.close()
    
    
    # configurations for cherrypy
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        }
    }
    
    #creating a thread to remove actors that are older than 60 sec
    Actor_removal(catalog_name, time_to_live)

    cherrypy.server.socket_host = host
    cherrypy.server.socket_port = port
    cherrypy.tree.mount (Catalog_config(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()