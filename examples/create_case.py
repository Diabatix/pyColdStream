#-------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#-------------------------------------------------------------------------------#

from coldstream import ColdstreamSession, case
import os

session = ColdstreamSession.create_from_login(user="admin@admin",
                                             password="admin",
                                              host="eu1")


print('Creating Case...')
P = session.projects.get_project(1586)
C = P.create_case(case.Case.CASE_TYPES["Simulation"], "Example Case")

print('done')
print('=====================================================')

print("Adding first  region...")
reg1 = C.create_region('region1')
geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'solid426161.step')
reg1.upload_geometry_file(geometry_file_path)
data =  {"physics": { "properties": { "id": 631, "name": "ST Collector solid", "rho": 8000, "Cp": 4500, "kappa": 80 }, "radiation": { "radiation": "disabled" } }, "sources": { "power": { "properties": { "Q": 25 }}}}
reg1.update("Housing", "solid", data)
print('done')
print('=====================================================')


print("Adding second region...")
reg2 = C.create_region('region2')
geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'fluid426160.step')
reg2.upload_geometry_file(geometry_file_path)
data = {"physics": { "properties": { "id": 1418, "name": "ST Collector fluid", "rho": 1000, "mu": 0.000959, "Cp": 4181, "kappa": 0.60567 }, "buoyancy": { "buoyancy": "disabled", "pref": 101325, "Tref": 293.15, "g": [] }, "radiation": { "radiation": "disabled" }, "turbulence": "kOmegaSST" }}
reg2.update("Fluid", "fluid", data)
print('done')
print('=====================================================')


print("Adding boundaries and subregion for second region...")
subreg1 = reg2.create_subregion("subreg1")
geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'standardDesign426163.step')
subreg1.upload_geometry_file(geometry_file_path)
data = {"sources": {}, "physics": { "properties": { "id": 525, "name": "ST Collector design", "rho": 8000, "Cp": 450, "kappa": 80 } }}
subreg1.update("Design", "design", data)

bound1 = reg2.create_boundary("boundary1")
geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'fixedFlowRateInlet426146.step')
bound1.upload_geometry_file(geometry_file_path)
data = {"properties": { "T": 293.15, "U": 4}}
bound1.update("Inlet", "fixedFlowRateInlet", data)



bound2 = reg2.create_boundary("boundary2")
geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'pressureOutlet426147.step')
bound2.upload_geometry_file(geometry_file_path)
data = {"properties": { "p": 2500 }}
bound2.update("Outlet", "pressureOutlet", data)

#Adding Target
T = C.create_target(bound2.ID)
d =  {"constraintType": "velocityVariance", "target": 100}
T.update("constraint", d)

print('done')
print('=====================================================')


print('Adding third region...')
reg3 = C.create_region('region3')
geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'solid426162.step')
reg3.upload_geometry_file(geometry_file_path)
data = {"physics": { "properties": { "id": 631, "name": "ST Collector solid", "rho": 8000, "Cp": 4500, "kappa": 80 }, "radiation": { "radiation": "disabled" } }, "sources": { "power": { "properties": { "Q": 25 }}}}
reg3.update("Heatsources", "solid", data)
print('done')
print('=====================================================')


print('Successfully created case')
print(f'Case ID: {C.ID}')