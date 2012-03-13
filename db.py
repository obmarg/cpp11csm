'''
This file contains the database code
'''

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

all = [
    'GetDbSession',
    'Compiler',
    'CompilerVersion',
    'Feature',
    'FeatureCompilerVersion'
    ]

# Switch this to true to enable debugging output
debug = False


engine = create_engine( 'sqlite:///data.db', echo=debug )
GetDbSession = sessionmaker( bind=engine )

Base = declarative_base()

class Compiler(Base):
    '''
    Class representing a compiler
    '''

    __tablename__ = "Compiler"

    id = Column( Integer, primary_key=True )
    name = Column( String )

class CompilerVersion(Base):
    '''
    Class representing an individual version of a compiler
    '''

    __tablename__ = "CompilerVersion"

    id = Column( Integer, primary_key=True )
    num = Column( String )
    compilerId = Column(
            Integer,
            ForeignKey( 
                'Compiler.id', onupdate='CASCADE', ondelete='CASCADE'
                )
            )
    compiler = relationship(
            'Compiler',
            backref=backref( 'versions', passive_deletes=True )
            )

class Feature(Base):
    '''
    Class representing an individual compiler feature
    '''

    __tablename__ = "Feature"

    id = Column( Integer, primary_key=True )
    name = Column( String )
    proposal = Column( String )
    link = Column( String )

class FeatureCompilerVersion(Base):
    '''
    Class linking features to their minimum compiler version
    '''

    __tablename__ = "FeatureCompilerVersion"

    id = Column( Integer, primary_key=True )
    featureId = Column(
            Integer, 
            ForeignKey( 
                'Feature.id', ondelete='CASCADE', onupdate='CASCADE'
                )
            )
    minimumVersionId = Column(
            Integer,
            ForeignKey(
                "CompilerVersion.id", ondelete="CASCADE", onupdate="CASCADE"
                )
            )

    feature = relationship( "Feature", backref="support" )
    minimumVersion = relationship( "CompilerVersion" )
