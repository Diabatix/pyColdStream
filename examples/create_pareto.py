#-------------------------------------------------------------------------------#
#
#                         --- C O L D S T R E A M api ---
#
#                                    EXAMPLE
#
#-------------------------------------------------------------------------------#

import matplotlib.pyplot as plt
from coldstream import ColdstreamSession

session = ColdstreamSession.create_from_login(user="admin@admin.com",
                                              password="admin",
                                              host="eu1")

projectID = 12345
caseID = 12345

P = session.projects.get_project(projectID)
C = P.get_case(caseID)

# Collect the data
C = P.get_case(case_ID)

for t in C.get_results_evolution_graph().data["targetGraphs"]:
    if t["targetType"] == "pressureLoss":
        x = [t_i["value"] for t_i in t["results"]]
        break
y = [r_i["value"] for r_i in C.get_results_evolution_graph().data["overallDesignPerformanceGraph"]["results"]]

plt.plot(x, y, marker='+', linestyle='', label=tag)

# Add grid and legend
plt.grid(True)
plt.legend()
plt.xlabel(r"$\Delta P$")
plt.ylabel(r"$J$")

# Save the figure as a PNG file
plt.savefig("pareto.png", dpi=300)
