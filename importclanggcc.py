#!/usr/bin/env python
'''
Imports the clang feature table into the database
'''

import sys
from bs4 import BeautifulSoup
from db import GetDbSession
from importutils import *

session = GetDbSession()


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
                utils.ProcessFeature( *details )

    session.commit()
