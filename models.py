import sqlalchemy.ext.declarative
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()

# Contracts Table
class Contracts (Base):
  __tablename__ = 'contracts'
  number = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
  owner = sqlalchemy.Column(sqlalchemy.String)
  prime = sqlalchemy.Column(sqlalchemy.String)
  prime_number = sqlalchemy.Column(sqlalchemy.String)
  # mm-dd-yyyy
  date = sqlalchemy.Column(sqlalchemy.String)
  name = sqlalchemy.Column(sqlalchemy.String)
  value = sqlalchemy.Column(sqlalchemy.Float)
  cost_types = sqlalchemy.Column(sqlalchemy.String)
  co_no = sqlalchemy.Column(sqlalchemy.Integer)
  description = sqlalchemy.Column(sqlalchemy.String)
  status = sqlalchemy.Column(sqlalchemy.String)
  # mm-dd-yyyy
  expiration_date = sqlalchemy.Column(sqlalchemy.String)
  comments = sqlalchemy.Column(sqlalchemy.String)

# Authorization Table
class Authorization (Base):
  __tablename__ = 'authorization'
  id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
  type = sqlalchemy.Column(sqlalchemy.String)
  contract_number = sqlalchemy.Column(sqlalchemy.String)
  auth_number = sqlalchemy.Column(sqlalchemy.String)
  # mm-dd-yyyy
  date = sqlalchemy.Column(sqlalchemy.String)
  value = sqlalchemy.Column(sqlalchemy.Float)
  status = sqlalchemy.Column(sqlalchemy.String)
  description = sqlalchemy.Column(sqlalchemy.String)
  # mm-dd-yyyy
  expiration_date = sqlalchemy.Column(sqlalchemy.String)
  comments = sqlalchemy.Column(sqlalchemy.String)

# Invoice Table
class Invoices (Base):
  __tablename__ = 'invoices'
  id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
  contract_number = sqlalchemy.Column(sqlalchemy.String)
  auth_number = sqlalchemy.Column(sqlalchemy.String)
  invoice_number = sqlalchemy.Column(sqlalchemy.String)
  # mm-dd-yyyy
  date = sqlalchemy.Column(sqlalchemy.String)
  period = sqlalchemy.Column(sqlalchemy.String)
  paid_amount = sqlalchemy.Column(sqlalchemy.Float)
  # mm-dd-yyyy
  paid_date = sqlalchemy.Column(sqlalchemy.String)
  description = sqlalchemy.Column(sqlalchemy.String)
  check_number = sqlalchemy.Column(sqlalchemy.String)
  comments = sqlalchemy.Column(sqlalchemy.String)

# Invoice Records Table
class InvoiceRecords (Base):
  __tablename__ = 'records'
  id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
  invoice_number = sqlalchemy.Column(sqlalchemy.String)
  project_manager = sqlalchemy.Column(sqlalchemy.String)
  address = sqlalchemy.Column(sqlalchemy.String)
  type = sqlalchemy.Column(sqlalchemy.String)
  task_description = sqlalchemy.Column(sqlalchemy.String)
  task_amount = sqlalchemy.Column(sqlalchemy.Float)
  percent_complete = sqlalchemy.Column(sqlalchemy.Integer)
  employee_name = sqlalchemy.Column(sqlalchemy.String)
  function = sqlalchemy.Column(sqlalchemy.String)
  contract_classification = sqlalchemy.Column(sqlalchemy.String)
  contract_cap = sqlalchemy.Column(sqlalchemy.Float)
  multiplier = sqlalchemy.Column(sqlalchemy.Float)
  billing_rate = sqlalchemy.Column(sqlalchemy.Float)
  hours = sqlalchemy.Column(sqlalchemy.Integer)
  invoiced_amount = sqlalchemy.Column(sqlalchemy.Float)

# Assignment Table
class Assignment (Base):
  __tablename__ = 'assignments'
  employee = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
  contract_no = sqlalchemy.Column(sqlalchemy.String)
  position = sqlalchemy.Column(sqlalchemy.String)
  current_rate = sqlalchemy.Column(sqlalchemy.Float)

# Employees Table
class Employees (Base):
  __tablename__ = 'employees'
  email = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
  name = sqlalchemy.Column(sqlalchemy.String)
  position = sqlalchemy.Column(sqlalchemy.String)
  authorization = sqlalchemy.Column(sqlalchemy.String)
  projects = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))

# Timesheet Table
class Timesheet (Base):
  __tablename__ = 'timesheet'
  # ID = email-YYYY-W##
  id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
  email = sqlalchemy.Column(sqlalchemy.String)
  # YYYY-W## is week
  week = sqlalchemy.Column(sqlalchemy.String)
  # days is 2D array of days with dates
  days = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))
  # hours is 2D array of projects by days, each is HH:MM
  hours = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))
  # description is 2D array of projects by days, each is a description
  description = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))  