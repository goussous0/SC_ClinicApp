#!/usr/bin/env python3

from pytm.pytm import TM, Server, Datastore, Dataflow, Boundary, Actor, Lambda, Data, Classification

tm = TM("my test tm")
tm.description = "another test tm"
tm.isOrdered = True


doctor = Actor("Doctor")
# doctor.inBoundary = User_Web


patient = Actor("Patient")
# patient.inBoundary = User_Web

registrar = Actor("Registrar")
# registrar.inBoundary = User_Web



web = Server("Web Server")
web.OS = "Debian"



db = Datastore("patients")
db.OS = "CentOS"
db.isHardened = False
# db.inBoundary = Web_DB
db.isSql = True
db.inScope = True
# db.sourceCode = "model/schema.sql"

tm.process()


