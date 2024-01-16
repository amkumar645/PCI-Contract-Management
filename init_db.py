# File to reset database when needed
import sqlalchemy
import sqlalchemy.orm
import models
import os

db_url = os.getenv("DATABASE_URL")

# Add test users
def add_test_contract(session):
  contract = models.Contracts(
    number = 1010585,
    owner = "Broward County Public Schools",
    prime = "ATKINS",
    prime_number = 1,
    # mm-dd-yyyy
    date = "03/17/21",
    name = "SMART Program Estimating and Project Controls",
    value = 5.15e6,
    cost_types = "CPFF",
    co_no = 1,
    description = "Review, analyze and provide recommendations for improvement of Atkins Monthly Reports.  Analyze other data related to processes that require improvement and provide recommendations",
    status = "Active",
    # mm-dd-yyyy
    expiration_date = "04/16/2024",
    comments = "Task Orders may be issued from date of this MSA award until the last day of the period and any options exercised."
  )
  session.add(contract)

def add_test_authorization(session):
  authorization = models.Authorization(
    id = "1010585-2",
    type = "TA",
    contract_number = 1010585,
    auth_number = 2,
    # mm-dd-yyyy
    date = "07/14/22",
    value =  89605.00,
    status = "Closed",
    description = "Review, analyze and provide recommendations for improvement of Atkins Monthly Reports.  Analyze other data related to processes that require improvement and provide recommendations",
    # mm-dd-yyyy
    expiration_date = "03/15/23",
  )
  session.add(authorization)

def add_test_invoice(session):
  invoice = models.Invoices(
    id="1010585-2-1",
    contract_number = 1010585,
    auth_number = 2,
    invoice_number = 1,
    # mm-dd-yyyy
    date = "08/12/22",
    period = "06/01/22-07/31/2022",
    paid_amount = 22543.92,
    # mm-dd-yyyy
    paid_date = "10/20/22",
    check_number = "ACH"
  )
  session.add(invoice)

def add_test_employee(session):
  employee = models.Employees(
    employee="amkumar@princeton.edu",
    position="Admin"
  )
  session.add(employee)
    
def main():
  # Create engine and drop and recreate all tables
  engine = sqlalchemy.create_engine(db_url)
  models.Base.metadata.drop_all(engine)
  models.Base.metadata.create_all(engine)

  with sqlalchemy.orm.Session(engine) as session:
    # Add fake test data if needed
    add_test_contract(session)
    add_test_authorization(session)
    add_test_invoice(session)
    add_test_employee(session)
    session.commit()

  engine.dispose()

if __name__ == '__main__':
  main()