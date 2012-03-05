'''
Defines some utilities for importing compiler support data
'''

from db import Compiler, CompilerVersion, Feature, FeatureCompilerVersion

all = [ 'Utils' ]

class Utils(object):
    '''
    Container class for utilities.
    Mostly just to save on passing in globals etc.
    '''

    def __init__( self, db, compilerName ):
        '''
        Constructor
        @param: db          The database to use
        @param: compiler    The compiler name
        '''
        self.db = db
        self.compiler = self.GetCompiler( compilerName )

    def GetCompiler( self, name ):
        '''
        Gets or creates a compiler with the passed in name
        '''
        try:
            compiler = self.db.query( Compiler ).filter_by( name=name ).one()
        except:
            compiler = Compiler( name = name )
            self.db.add( compiler )
            self.db.commit()
        return compiler

    def GetVersion( self, verString ):
        '''
        Gets/creates a version from database
        @param: verString   The version string (with a possible prefix)
        '''
        prefix = self.compiler.name + " "
        if verString.startswith( prefix ):
            verString = verString.replace( prefix, "" ).strip()
        #TODO: Need to handle Yes + other oddball strings here
        try:
            verEntry = self.db.query( CompilerVersion ).filter_by(
                    compiler = self.compiler,
                    num = verString
                    ).one()
        except:
            verEntry = CompilerVersion(
                    compiler = self.compiler,
                    num = verString
                    )
            self.db.add( verEntry )
            self.db.commit()
        return verEntry

    def ProcessFeature( self, name, proposal, version ):
        '''
        Processes a feature extracted from the table
        @param: name - The name of the feature
        @param: proposal - The proposal number
        @param: version - The version string avaliable from (or "No")
        '''
        # First, check if we have a feature with this proposal number
        proposals = self.db.query( 
                Feature 
                ).filter_by( proposal = proposal ).all()
        if not proposals:
            # We don't, so lets create one:
            feature = Feature( 
                    name = name,
                    proposal = proposal,
                    link = ""
                    )
            self.db.add( feature )
        else:
            if len( proposals ) > 1:
                raise Exception( 
                        "Too many existing proposals {}".format( proposal )
                        )
            feature = proposals[ 0 ]

        if version.beginswith( "No" ):
            return # We don't need to add a version entry if there's no support

        foundOurCompiler = False
        for support in feature.support:
            if support.minimumVersion.compiler == self.compiler:
                foundOurCompiler = True

        if not foundOurCompiler:
            verEntry = self.GetVersion( version )
            feature.support.append(
                    FeatureCompilerVersion( minimumVersion = verEntry )
                    )
