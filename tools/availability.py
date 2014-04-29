import socket
import re
from urllib import request

import requests


class InternetNotReachable(Exception):
    """Exception raised when google and yahoo are not reachable.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self,  message='Internet not reachable'):
        self.message = message


class InvalidHostname(Exception):
    """Exception raised when google and yahoo are not reachable.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self,  message='Invalid hostname'):
        self.message = message


def normalize_url(url):
    """If a url doesn't have a http/https prefix, add http://"""
    if not re.match('^http[s]?://', url):
        url = 'http://' + url
    return url


def get_hostname(url):
    """If a url have a http/https prefix, get rid of it"""
    if re.match('^http://', url):
        url = url[7:]
    elif re.match('^https://', url):
        url = url[8:]
    return url


def check_connectivity(reference):
    try:
        request.urlopen(reference, timeout=1)
        return True
    except request.URLError:
        return False
    except socket.timeout:
        return False


def is_hostname_valid(hostname):
    print("hostname=" + hostname)
    try:
        socket.gethostbyname(hostname)
        return True
    except OSError:
        return False


def is_internet_reachable():
    """Checks Google then Yahoo just in case one is down"""
    google_ip1 = check_connectivity('http://173.194.70.113')
    if not google_ip1:
        google_ip2 = check_connectivity('http://173.194.113.36')
        if not google_ip2:
            return False
    return True


def get_response_code(url):
    try:
        r = requests.head(url)
        return r.status_code, r.status_code in range(200, 302)
        #prints the int of the status code. Find more at httpstatusrappers.com :)
    except ConnectionError:
        return 0, False


def is_up(watcher):
    if is_internet_reachable():
        if is_hostname_valid(get_hostname(watcher.url())):
            http_code, up = get_response_code(normalize_url(watcher.url()))
            print("URL=" + watcher.url(), "Code=" + str(http_code))
            return up
        else:
            print(InvalidHostname)
            raise InvalidHostname()
    else:
        print(InternetNotReachable)
        raise InternetNotReachable()