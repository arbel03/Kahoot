import httplib
import json


def update(name='local', ip=None, port=None, host='planq.ddns.net', host_port=17011):
    '''
    Update your kahoot server information on the directory server.

    Parameters:
    name : str
        Your name. Used to identify your server in the database.
    ip : str 
        Your server's IP address.
    port : str
        Your server's port.
    host : str
        The directory server's domain name. (Default - 'planq.ddns.net')
    host_port : int
        The directory server's port. (Default - 17011)

    Returns:
    response : {
        'status' : str - query status
    }
    query statuses:
    'OK' - If the command was completed successfully
    'invalid request' - If the request was invalid
    'internal server error' - If an unknown server error has occurred
    '''
    server = httplib.HTTPConnection('{0}:{1}'.format(host, host_port))
    data = {
        'ip': ip,
        'port': str(port),
        'name': name
    }
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    server.request('POST', '/update', json.dumps(data), headers)
    response = json.loads(server.getresponse().read())
    return response


def get_details(name='local', host='planq.ddns.net', host_port=17011):
    '''
    Returns a dictionary with the ip and the port of the requested
    server's name.

    Parameters:
    name : str
        Your name. Used to identify your server in the database.
    host : str
        The directory server's domain name. (Default - 'planq.ddns.net')
    host_port : int
        The directory server's port. (Default - 17011)

    Returns:
    result : {
            'result' : {
                'name' : str - name of the server's owner,
                'ipaddr' : str - ip of the server,
                'port' : str - port of the server
            },
            'status' : str - query status
        }
    query statuses:
    'OK' - If the command was completed successfully
    'invalid request' - If the request was invalid
    'internal server error' - If an unknown server error has occurred
    '''
    server = httplib.HTTPConnection('{0}:{1}'.format(host, host_port))
    data = {
        'name': name
    }
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    server.request('POST', '/get', json.dumps(data), headers)
    result = json.loads(server.getresponse().read())
    return result


if __name__ == '__main__':
    print 'Welp...'