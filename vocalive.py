#!/usr/bin/env python

import argparse;
import requests;
from bs4 import BeautifulSoup;
import os;
import sys;
# -*- coding: utf-8 -*-

class Manager:
    """ Manages bots and labs """
    args = '';
    bots = list();

    def __init__(self):
        """ Where everything begins... """
        parser = argparse.ArgumentParser( description='Live Vocabulary Observer' );
        parser.add_argument( '-m', metavar='Length', default=2, help='Word minimum length. Default = 2' );
        parser.add_argument( '-o', '--output', metavar='File', help='File to save learned words' );
        parser.add_argument( 'url', metavar='Address', help='Web address to learn from' );
        self.args = parser.parse_args();

    def request_page( self ):
        self.createbot( self.args.url );

    def createbot( self, url ):
        self.bots.append( Bot( self, url ) );

    def write_words( self, text, encoding ):
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
        answer = '';
        try:
            self.headers = {'Accept-Charset': 'utf-8'}
            self.answer = requests.get( self.address, params=self.headers )
            if (self.answer.status_code != 200):
                raise IOError
            self.souped_page = BeautifulSoup(self.answer.text, 'html.parser');
            for script in self.souped_page(["script", "style"]):
                script.extract()
            self.souped_page = BeautifulSoup(str(self.souped_page), 'html.parser');
            self.text = self.souped_page.get_text();
            self.send_to_lab()
            exit();
        except IOError: 
            end('Request returned ' + str(self.answer.status_code) + ' code');
        

    def send_to_lab( self ):
        lab = Laboratory( self.manager, self.text, self.answer.encoding );

class Laboratory:
    """ Text processing """

    manager = str();
    text = str();
    encoding = str();
    wordlist = set();
    count = int();

    def __init__( self, manager, text, encoding ):
        self.manager = manager;
        self.encoding = encoding;
        self.analyse( text.lower() );


    def analyse( self, text ):
        separated_words = self.breakdown( text );
        clean_words = self.strip_punctuation( separated_words );
        unaccented = self.strip_accentuation( clean_words );
        unique_words = self.discard_repetition( unaccented );
        eligible_words = self.minimum_length( unique_words, self.manager.args.m );
        sorted_strings = self.sort_data( eligible_words );
        self.wordlist = self.digits_out( sorted_strings ); 
        self.count = self.count_words( self.wordlist );
        self.manager.get_results( self.wordlist, self.encoding );
        

    def breakdown( self, text ):
        text = self.convert_to_space( text );
        return text.split();

    def strip_punctuation( self, text ):
        treated = list();
        for word in text:
            treated.append( self.remove_chars( word ) );
        return treated;

    def convert_to_space( self, string ):
        space_chars = { ord('.'): ord(' '), 
                        ord('_'): ord(' '),
                        ord('/'): ord(' '),
                        ord('-'): ord(' ')};
        return string.translate( space_chars );

    def remove_chars(self, string ):
        blocked_chars = { ord('!'): None,
                          ord('\"'): None,
                          ord('#'): None,
                          ord('$'): None,
                          ord('%'): None,
                          ord('&'): None,
                          ord('\''): None,
                          ord('('): None,
                          ord(')'): None,
                          ord('*'): None,
                          ord('+'): None,
                          ord(','): None,
                          ord(':'): None,
                          ord(';'): None,
                          ord('<'): None,
                          ord('='): None,
                          ord('>'): None,
                          ord('?'): None,
                          ord('@'): None,
                          ord('['): None,
                          ord('\\'): None,
                          ord(']'): None,
                          ord('^'): None,
                          ord('`'): None,
                          ord('{'): None,
                          ord('|'): None,
                          ord('}'): None,
                          ord('~'): None,
                          ord('\xa9'): None,
                          ord('\xaa'): None,
                          ord('\xab'): None,
                          ord('\xae'): None,
                          ord('\xb0'): None,
                          ord('\xb2'): None,
                          ord('\xb3'): None,
                          ord('\xba'): None,
                          ord('\xbb'): None,
                          ord('\xb9'): None};
        return string.translate( blocked_chars );

    def strip_accentuation( self, string ):
        treated = list();
        for word in string:
            treated.append( self.translate_accents( word ) );
        return treated;

    def translate_accents( self, string ):
        accents = { 
                    ord('\xe7'): u'c',
                    ord('\xc0'): ord('A'),
                    ord('\xc0'): ord('A'),
                    ord('\xc1'): ord('A'),
                    ord('\xc2'): ord('A'),
                    ord('\xc3'): ord('A'),
                    ord('\xc8'): ord('E'),
                    ord('\xc9'): ord('E'),
                    ord('\xca'): ord('E'),
                    ord('\xcc'): ord('I'),
                    ord('\xcd'): ord('I'),
                    ord('\xce'): ord('I'),
                    ord('\xd2'): ord('O'),
                    ord('\xd3'): ord('O'),
                    ord('\xd4'): ord('O'),
                    ord('\xd5'): ord('O'),
                    ord('\xd9'): ord('U'),
                    ord('\xda'): ord('U'),
                    ord('\xdb'): ord('U'),
                    ord('\xdc'): ord('U'),
                    ord('\xe0'): ord('a'),
                    ord('\xe1'): ord('a'),
                    ord('\xe2'): ord('a'),
                    ord('\xe3'): ord('a'),
                    ord('\xe8'): ord('e'),
                    ord('\xe9'): ord('e'),
                    ord('\xea'): ord('e'),
                    ord('\xec'): ord('i'),
                    ord('\xed'): ord('i'),
                    ord('\xee'): ord('i'),
                    ord('\xf1'): ord('n'),
                    ord('\xf2'): ord('o'),
                    ord('\xf3'): ord('o'),
                    ord('\xf4'): ord('o'),
                    ord('\xf5'): ord('o'),
                    ord('\xf9'): ord('u'),
                    ord('\xfa'): ord('u'),
                    ord('\xfb'): ord('u'),
                    ord('\xfc'): ord('u')};
        return string.translate( accents );
 

    def discard_repetition( self, words ):
        temp = set();
        for word in words:
            if( not temp.__contains__( word ) ):
                temp.add( word );
        return temp;

    def minimum_length( self, words, number=2 ):
        minimum_length = int( number );
        temp = set();
        for word in words:
            if( len( word ) >= minimum_length ):
                temp.add(word);
        return temp;
            

    def sort_data( self, unique ):
        return sorted( unique ); 

    def digits_out( self, strings ):
        treated = list();
        for word in strings:
            if( not word.isdigit() ):
                treated.append( word );
        return treated;

    def count_words( self, words ):
        number = int();
        number = len( words );
        print('Unique words = ' + str( number ) );
        return number;


def end( reason ):
    print('\n[-] ' + reason);
    exit();

if __name__ == "__main__":

    observer = Manager();
    observer.request_page();

