#!/usr/bin/env python
'''
Imports the clang feature table into the database
'''

import sys
import re
from bs4 import BeautifulSoup
from db import GetDbSession
from importutils import *

session = GetDbSession()

getVerRegexp = re.compile( r'GCC\s+(\d+\.\d+)' )

def SanitiseGCCName( name ):
    '''
    GCCs table isn't as neat as the Clang one, so this function modifies
    the GCC version name to eliminate excess "versions"
    @param: name    The input version name
    @return         A sanitised name
    '''
    if name == 'Yes':
        return 'GCC 4.3' # Yes = all, so use lowest known version
    if name.startswith( 'Some development' ):
        return "No"
    match = getVerRegexp.match( name )
    if match:
        return 'GCC ' + match.group( 1 )
    return name



if __name__ == "__main__":
    if len( sys.argv ) != 2:
        quit( "Usage: importclanggcc.py [compilername]" )
    if sys.argv[ 1 ] != "Clang" and sys.argv[ 1 ] != "GCC":
        quit( "Compiler name must be either Clang or GCC" )
    
    utils = Utils( session, sys.argv[ 1 ] )
    
    soup = BeautifulSoup( sys.stdin )

    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            details = []
            for cell in row.find_all('td'):
                details.append( cell.get_text() )
            if details:
                if sys.argv[ 1 ] == 'GCC':
                    details[ 2 ] = SanitiseGCCName( details[ 2 ] )
                utils.ProcessFeature( *details )

    session.commit()
