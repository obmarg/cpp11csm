'''
Imports the clang feature table into the database
'''

import sys
from bs4 import BeautifulSoup
from db import GetDbSession,Compiler
from importutils import *

session = GetDbSession()
#TODO: Create clang compiler if not already there
try:
    compiler = session.query( Compiler ).filter_by( name="Clang" ).one()
except:
    compiler = Compiler( name = "Clang" )
    session.add( compiler )
    session.commit()

utils = Utils( session, compiler )

if __name__ == "__main__":
    soup = BeautifulSoup( sys.stdin )

    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            details = []
            for cell in row.find_all('td'):
                details.append( cell.get_text() )
            if details:
                utils.ProcessFeature( *details )

    session.commit()
