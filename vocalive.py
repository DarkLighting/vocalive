#!/usr/bin/env python

import argparse;
import requests;
from bs4 import BeautifulSoup;

class Manager:
    """ Manages bots """
    args = '';
    bots = list();

    def __init__(self):
        """ Where everything begins... """
        
        parser = argparse.ArgumentParser( description='Live Vocabulary Observer' );
        parser.add_argument( 'url', help='Web address to learn from' );
        parser.add_argument( '-o', help='File to save learned words' );
        self.args = parser.parse_args();

    def learn(self):
        self.bots.append( Bot(self.args.url) );

class Bot:
    """ Crawler """
    address = ''; 
    session = '';

    def __init__(self, url):
        self.address = url;
        self.fetch();
        print(self.address);

    def check_url(self):
        if ((self.address.find('http://',0,7) == -1) and (self.address.find('https://',0,8) == -1)):
            end('ERROR: address not starting with http or https.\n\tCheck your URL and try again.\n');

    def fetch(self):
        self.check_url();
        


def end( reason ):
    print '\n[-] ' + reason;
    exit();

if __name__ == "__main__":
    observer = Manager();
    observer.learn();

