
import codecs
import jinja2
from db import GetDbSession, Compiler, CompilerVersion, Feature
from db import FeatureCompilerVersion
from fabric.api import local, run


def generate():
    '''
    Generates HTML from the database
    '''
    session = GetDbSession()
    featureQuery = session.query( Feature ).join( 'support', 'minimumVersion' )
    compilerQuery = session.query( Compiler ).join( 'versions' )
    featureList = []
    compilerList = []
    for compiler in compilerQuery:
        verList = []
        compilerList.append({
                'name' : compiler.name, 
                'shortname' : compiler.name.replace( ' ', '' ),
                'versions' : verList
                })
        for ver in compiler.versions:
            verList.append( 
                    { 'num' : ver.num, 'altnum' : ver.num.replace( '.', '_' ) } 
                    )
    featureList = []
    for feature in featureQuery:
        supportList = []
        featureList.append({
                'name' : feature.name,
                'support' : supportList
                })
        minVersions = {}
        for featureSupport in feature.support:
            try:
                minVer = featureSupport.minimumVersion
                minVersions[ minVer.compiler.name ] = float( minVer.num )
            except ValueError:
                pass
        for compiler in compilerQuery:
            for ver in compiler.versions:
                compId = (
                        compiler.name.replace( ' ', '' ) +
                        ver.num.replace( '.', '_' )
                        )
                supportDict = { 'id' : compId }

                try:
                    try:
                        supported = ( 
                                float( ver.num ) >= minVersions[ compiler.name ]
                                )
                    except ValueError:
                        # Fall back for "SVN" version of Clang
                        if ver.num == "SVN" and minVersions[ compiler.name ]:
                            # If supported at all, supported in SVN
                            supported = True 
                        else:
                            supported = False
                except KeyError:
                    supported = False
                supportDict[ 'supported' ] = supported
                supportList.append( supportDict )
    templateData = {
            'compilers' : compilerList,
            'features' : featureList
            }
    env = jinja2.Environment( loader=jinja2.FileSystemLoader( 'templates' ) )
    template = env.get_template( 'index.html' )
    with codecs.open( 'web/index.html', encoding='utf-8', mode='w' ) as output:
        output.write( 
                template.render( **templateData ) 
                )

def coffee():
    local( 'coffee -o web/js/ coffeescript/' )
