from sqlalchemy.orm import declarative_base

Base = declarative_base()
"""
The declarative base class for SQLAlchemy.

This class is created using SQLAlchemy's declarative_base function, which returns
a base class for declarative class definitions. The 'Base' class is then used to
create new ORM (Object-Relational Mapping) classes in SQLAlchemy. Each ORM class
represents a table in the database and inherits from this base class, allowing
SQLAlchemy to recognize it and map it to the database appropriately.
"""
