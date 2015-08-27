#!/usr/bin/env python

import argparse;
import requests;
from bs4 import BeautifulSoup;
import os;
import sys;
# -*- coding: utf-8 -*-

class Manager:
    """ Manages bots """
    args = '';
    bots = list();

    def __init__(self):
        """ Where everything begins... """
        parser = argparse.ArgumentParser( description='Live Vocabulary Observer' );
        parser.add_argument( '-m', metavar='Length',  help='Word minimum length' );
        parser.add_argument( '-o', '--output', metavar='File', default=2, help='File to save learned words' );
        parser.add_argument( 'url', metavar='Address', help='Web address to learn from' );
        self.args = parser.parse_args();

    def request_page( self ):
        self.createbot( self.args.url );

    def createbot( self, url ):
        self.bots.append( Bot( self, url ) );

    def write_words( self, text, encoding ):
        print encoding;
        try:
            with open( self.args.output, 'w+' ) as content:
                    for word in text:
                        content.write( word.encode( encoding, errors='replace' )+'\n' );
        except IOError as e:
            end("I/O error({0}): {1}".format(e.errno, e.strerror));

    def get_results( self, text, encoding ):
        self.write_words( text, encoding );

class Bot:
    """ Crawler """
    manager = '';
    address = ''; 
    answer = '';
    text = '';

    def __init__(self, owner,  url):
        self.manager = owner;
        self.address = url;
        self.fetch();
        print(self.address);

    def check_url(self):
        if ((self.address.find('http://',0,7) == -1) and (self.address.find('https://',0,8) == -1)):
            end('ERROR: address not starting with http or https.\n\tCheck your URL and try again.\n');

    def fetch(self):
        self.check_url();
        try:
            self.headers = {'Accept-Charset': 'utf-8'}
            self.answer = requests.get( self.address, params=self.headers )
            if (self.answer.status_code != 200):
                raise IOError
            self.souped_page = BeautifulSoup(self.answer.text, 'html.parser');
            self.text = self.souped_page.get_text();
            self.send_to_lab()
            exit();
        except IOError: 
            end('Request returned ' + str(self.answer.status_code) + ' code');
        

    def send_to_lab( self ):
        lab = Laboratory( self.manager, self.text, self.answer.encoding );

class Laboratory:
    """ Text processing """

    manager = '';
    text = '';
    encoding = '';
    wordlist = set();
    count = int();

    def __init__( self, manager, text, encoding ):
        self.manager = manager;
        self.encoding = encoding;
        self.analyse( text );


    def analyse( self, text ):
        separated_words = self.breakdown( text );
        unique_words = self.discard_repetition( separated_words );
        eligible_words = self.minimum_length( unique_words, self.manager.args.m );
        self.wordlist = self.sort_data( eligible_words ); 
        self.count = self.count_words( self.wordlist );
        self.manager.get_results( self.wordlist, self.encoding );
        

    def breakdown( self, text ):
        return text.split();

    def discard_repetition( self, words ):
        temp = set();
        for word in words:
            if( not temp.__contains__( word ) ):
                temp.add( word );
        return temp;

    def minimum_length( self, words, number ):
        minimum_length = int( number );
        temp = set();
        print minimum_length;
        for word in words:
            if( len( word ) >= minimum_length ):
                temp.add(word);
        return temp;
            

    def sort_data( self, unique ):
        return sorted( unique ); 

    def count_words( self, words ):
        number = int();
        number = len( words );
        print('Unique words = ' + str( number ) );
        return number;


def end( reason ):
    print '\n[-] ' + reason;
    exit();

if __name__ == "__main__":

    observer = Manager();
    observer.request_page();

