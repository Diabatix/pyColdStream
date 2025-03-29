#-------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#-------------------------------------------------------------------------------#

from coldstream import ColdstreamSession, case
import os
import time

session = ColdstreamSession.create_from_login(user="maarten.haine@diabatix.com",
                                              password="msY#xJ!t#gig4heq",
                                              host="stage.helios")

P = session.projects.get_project(1586)
"""C = P.create_case(case.Case.CASE_TYPES["Simulation"], "Demo2")
"""

C = P.get_case(5441)
R = C.create_region('region1')
Region_id = R.ID
print(R)
geometry_file_path = os.path.join(os.path.dirname(__file__), 'solid', 'geometry.step')
R.upload_geometry_file(geometry_file_path)
print(R)

data = {'physics': {'properties': {'id': 350, 'name': '0177_Plexi', 'rho': 118, 'Cp': 147, 'kappa': 0.2}, 'radiation': {'radiation': 'disabled'}}, 'sources': {'power': {'properties': {'Q': 120}}}}
R.update("reg1", "solid", data)

R = C.get_region(Region_id)
print(R)

SR = R.create_boundary("subreg1")
heated_wall_path = os.path.join(os.path.dirname(__file__), 'solid', 'heatedWall.step')
SR.upload_geometry_file(heated_wall_path)
print('now SR')
print(SR)
print(SR.ID)
SR_ID = SR.ID
data = {'properties': {'Q': None, 'emissivity': 0.9, 'absorptivity': 0.9}}
print("this error is update")
SR.update("heated_wall", "solid", data)
print(SR)
print("this error is not update")
SR = R.get_subregion(SR_ID)
print(SR)


"""C = P.get_case(5436)
R = C.regions[0]
data = {'physics': {'properties': {'id': 350, 'name': '0177_Plexi', 'rho': 118, 'Cp': 147, 'kappa': 0.2}, 'radiation': {'radiation': 'disabled'}}, 'sources': {'power': {'properties': {'Q': 120}}}}
print("ok")
print(R)
print("ok")
R.update("reg1", "solid", data)
heated_wall_path = os.path.join(os.path.dirname(__file__), 'solid', 'heatedWall.step')
print(R)
SR = R.create_subregion("heatedWall")
print(SR)
SR.upload_geometry_file(heated_wall_path)
print(SR)"""

