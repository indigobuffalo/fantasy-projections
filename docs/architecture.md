main.py
  - like a routes file, just passes args to controller

controller
  - determines what path to take given args
    - what leauge / svc
    - what type of lookup, filtering

service 
  - instantiates daos
  - common daos + league specific

daos
  - read data from db, excel, etc
  
  