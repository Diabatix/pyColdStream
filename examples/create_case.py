#-------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#-------------------------------------------------------------------------------#

from coldstream import ColdstreamSession, Case

session = ColdstreamSession.create_from_login(user="admin@admin.com",
                                              password="admin",
                                              host="eu1")

P = session.projects.get_project(ID=12345)
C = P.create_case(Case.CASE_TYPES["Simulation"], "Demo simulation")
