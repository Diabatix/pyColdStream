#-------------------------------------------------------------------------------#
#
#                         --- C O L D S T R E A M api ---
#
#                                    EXAMPLE
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
