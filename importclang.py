'''
Imports the clang feature table into the database
'''

import sys
from bs4 import BeautifulSoup
from db import *

session = GetDbSession()
#TODO: Create clang compiler if not already there
try:
    compiler = session.query( Compiler ).filter_by( name="Clang" ).one()
except:
    compiler = Compiler( name = "Clang" )
    session.add( compiler )
    session.commit()

def GetVersion( verString ):
    '''
    Gets/creates a version from database
    @param: verString   The version string (with Clang prepended probably)
    '''
    if verString.startswith( "Clang " ):
        verString = verString.replace( "Clang ", "" ).strip()
    try:
        verEntry = session.query( CompilerVersion ).filter_by(
                compiler = compiler,
                num = verString
                ).one()
    except:
        verEntry = CompilerVersion(
                compiler = compiler,
                num = verString
                )
        session.add( verEntry )
        session.commit()
    return verEntry


def ProcessFeature( name, proposal, version ):
    '''
    Processes a feature extracted from the table
    @param: name - The name of the feature
    @param: proposal - The proposal number
    @param: version - The version string of the proposal
    '''
    # First, check if we have a feature with this proposal number
    proposals = session.query( 
            Feature 
            ).filter_by( proposal = proposal ).all()
    if not proposals:
        # We don't, so lets create one:
        feature = Feature( 
                name = name,
                proposal = proposal,
                link = ""
                )
        session.add( feature )
    else:
        if len( proposals ) > 1:
            raise Exception( 
                    "Too many existing proposals {}".format( proposal )
                    )
        feature = proposals[ 0 ]

    if version == "No":
        return # We don't need to add a version entry if there's no support

    foundOurCompiler = False
    for support in feature.support:
        if support.minimumVersion.compiler == compiler:
            foundOurCompiler = True

    if not foundOurCompiler:
        verEntry = GetVersion( version )
        feature.support.append(
                FeatureCompilerVersion( minimumVersion = verEntry )
                )


if __name__ == "__main__":
    soup = BeautifulSoup( sys.stdin )

    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            details = []
            for cell in row.find_all('td'):
                details.append( cell.get_text() )
            if details:
                ProcessFeature( *details )

    session.commit()
