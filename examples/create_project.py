#-------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#-------------------------------------------------------------------------------#

from coldstream import ColdstreamSession
from pprint import pprint

session = ColdstreamSession.create_from_login(user="admin@admin.com",
                                              password="admin",
                                              host="eu1")

new_project = session.projects.create_project("Project Name",
                                              "This is the project description.")

pprint(new_project.data)
