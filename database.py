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

# Get contract by contract number
def get_contract_by_number(number) -> models.Contracts:
  contract = None
  with sqlalchemy.orm.Session(engine) as session:
    contract = session.query(models.Contracts).filter(
        models.Contracts.number == number).first()
  return contract

#----------------------------------------------------------------------
# Authorization Queries
#----------------------------------------------------------------------
# Get all authorizations
def get_all_authorizations() -> List[models.Authorization]:
  auths = []
  with sqlalchemy.orm.Session(engine) as session:
    auths = session.query(models.Authorization).order_by(
      models.Authorization.id,
      models.Authorization.date.desc()
    ).all()
  return auths

# Get all authorizations by contract number
def get_all_authorizations_by_contract_number(number) -> List[models.Authorization]:
  auths = []
  with sqlalchemy.orm.Session(engine) as session:
    auths = session.query(models.Authorization).filter(
      models.Authorization.contract_number == number).all()
  return auths

#----------------------------------------------------------------------
# Invoice Queries
#----------------------------------------------------------------------
# Get all invoices
def get_all_invoices() -> List[models.Invoices]:
  invoices = []
  with sqlalchemy.orm.Session(engine) as session:
    invoices = session.query(models.Invoices).order_by(
      models.Invoices.id,
      models.Invoices.date.desc()
    ).all()
  return invoices

# Get all authorizations by contract number
def get_all_invoices_by_contract_number(number) -> List[models.Invoices]:
  invoices = []
  with sqlalchemy.orm.Session(engine) as session:
    invoices = session.query(models.Invoices).filter(
      models.Invoices.contract_number == number).all()
  return invoices