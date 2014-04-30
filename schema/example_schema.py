from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine, MetaData, Date, DateTime, Float, Boolean
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker, relation
from sqlalchemy.ext.declarative import declarative_base 

import sqlalchemy

##########################################################################################
####### ADD NEW DATABASE TABLE ENTRIES HERE ##############################################
##########################################################################################

class ExampleStatus(Base):

    __tablename__   = 'free_example_status'
    
    # Primary Record Entries:
    id              = Column(Integer, primary_key = True)
    example_status  = Column(String(30))

    # Foreign Key Example:

# end of ExampleStatus


class ExampleMasterRecords(Base):

    __tablename__                   = 'example_master_table'

    # Primary Record Entries:
    id                              = Column(Integer, primary_key=True)
    example_string                  = Column(String(80))
    example_date                    = Column(DateTime)
    example_float                   = Column(Float)
    example_integer                 = Column(Float)

    # Foreign Key Example:
    example_symbol_id               = Column(Integer, ForeignKey(ExampleStatus.id))
    example_symbol_id_relationship  = relationship(ExampleStatus)

# end of ExampleMasterRecords

