#!/usr/bin/env python
'''
Imports the MSVC feature table into the database
'''

import sys
import re
from bs4 import BeautifulSoup
from db import GetDbSession
from importutils import Utils

session = GetDbSession()

class Feature(object):
    ''' Class used for processing one line of the MSVC table '''
    urlRegexp = re.compile( r'(n\d+)\.((html?)|(pdf))' )
    verNumRegexp = re.compile( r'v\d+\.\d+' )
    descRegexp = re.compile( r'(.+?) v\d+.\d+' )
    defectRegexp = re.compile( r'.html#(\d+)$' )

    def __init__( self, desc, links, vc10, vc11 ):
        '''
        Constructor
        @param: desc    The description text
        @param: links   The links from the description
        @param: vc10    The vc10 support text
        @param: vc11    The vc11 support text
        '''
        self.desc = desc
        self.links = links
        print "Processing " + desc
        self.vc10 = self.ProcessText( vc10 )
        self.vc11 = self.ProcessText( vc11 )
        self.samesupport = (
                self.vc10 and self.vc11 and self.vc10[ 1 ] == self.vc11[ 1 ]
                )

    def ProcessText( self, text ):
        '''
        Processes the text from the VC10/11 support column 
        @param: text    The text to process
        @return         An array: [ Text, proposalnumber ] or none
        '''
        print "Text: " + text
        if text == "No" or text == "N/A":
            print "Is No"
            return None
        if text == "Partial":   # Treat partial as no for now
            print "Is Partial, skipping"
            return None
        if text == "TR1":       # Treat TR1 as no for now
            print "Is TR1, skipping"
            return None
        #TODO: Need to handle "TR1"
        if text == "Yes":
            print "Is Simple Yes"
            return [ self.desc, self.ProcessUrl( self.links[0]['href'] ) ]
        # Now the awkward case, when there's v0.blah to consider
        match = self.verNumRegexp.search( text )
        assert match
        verNum = match.group( 0 )
        # So, lets find the link that has this version number
        proposal = None
        for link in self.links:
            if link.get_text() == verNum:
                proposal = self.ProcessUrl( link[ 'href' ] )
                break
        assert proposal
        # Get the clean description, and append the version number
        # to differentiate from other versions
        match = self.descRegexp.search( self.desc )
        desc = '{} {}'.format( match.group( 1 ), verNum )
        return [ desc, proposal ]

    def ProcessUrl( self, url ):
        '''
        Gets a proposal number from the supplied URL
        '''
        print url
        match = self.urlRegexp.search( url )
        if not match:
            # Find the defect number instead
            match = self.defectRegexp.search( url )
            return 'B' + match.group( 1 )
        return match.group( 1 ).upper()

if __name__ == "__main__":
    utils = Utils( session, "Visual Studio" )
    
    soup = BeautifulSoup( sys.stdin )

    for table in soup.find_all('table'):
        # There's 3 tables we want, then at least another 2 we don't
        # afterwards, so skip over some tables
        for row in table.find_all('tr')[1:]:
            details = []
            cells =  row.find_all('td')
            assert len( cells ) == 3
            f = Feature( 
                    cells[ 0 ].get_text(), 
                    cells[ 0 ].find_all( 'a' ),
                    cells[ 1 ].get_text(),
                    cells[ 2 ].get_text()
                    )
            if f.samesupport or f.vc10:
                # If Same support on both compilers, submit vc10 as the 
                # minimum version
                utils.ProcessFeature(
                        f.vc10[ 0 ],
                        f.vc10[ 1 ],
                        '10'
                        )
            if f.vc10 and not f.samesupport:
                    utils.ProcessFeature(
                            f.vc11[ 0 ],
                            f.vc11[ 1 ],
                            '11'
                            )

    session.commit()
