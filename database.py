from typing import List
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
import models
import os

# Database URL
db_url = os.getenv("DATABASE_URL")
# Global engine to use
engine =  sqlalchemy.create_engine(db_url, pool_pre_ping=True)

#----------------------------------------------------------------------
# Employee queries
#----------------------------------------------------------------------
# Get user from netid
def get_employee(id) -> models.Employees:
  # Make sure to only get one user
  employee = None
  with sqlalchemy.orm.Session(engine) as session:
    employee = session.query(models.Employees).filter(
      models.Employees.email == id).first()
  return employee

# Add employee to database
def add_employee(employee:models.Employees):
  with sqlalchemy.orm.Session(engine) as session:
    session.add(employee)
    session.commit()

#----------------------------------------------------------------------
# Contract Queries
#----------------------------------------------------------------------
# Get all contracts
def get_all_contracts() -> List[models.Contracts]:
  contracts = []
  with sqlalchemy.orm.Session(engine) as session:
    contracts = session.query(models.Contracts).order_by(
      models.Contracts.number,
      models.Contracts.date.desc()
    ).all()
  return contracts