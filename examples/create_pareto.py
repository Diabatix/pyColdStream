#-------------------------------------------------------------------------------#
#
#                         --- C O L D S T R E A M api ---
#
#                                    EXAMPLE
#
#-------------------------------------------------------------------------------#

import matplotlib.pyplot as plt
from pycoldstreamv0_3.coldstream import ColdstreamSession

session = ColdstreamSession.create_from_login(user="admin@admin.com",
                                              password="admin",
                                              host="eu1")

projectID = 1550
caseID = 5429

P = session.projects.get_project(projectID)
C = P.get_case(caseID)

# Collect the data
C = P.get_case(caseID)

for t in C.get_results_evolution_graph().data["targetGraphs"]:
    if t["targetType"] == "pressureLoss":
        x = [t_i["value"] for t_i in t["results"]]
        break
y = [r_i["value"] for r_i in C.get_results_evolution_graph().data["overallDesignPerformanceGraph"]["results"]]

plt.plot(x, y, marker='+', linestyle='', label="title pareto")

# Add grid and legend
plt.grid(True)
plt.legend()
plt.xlabel(r"$\Delta P$")
plt.ylabel(r"$J$")

plt.ticklabel_format(style="plain", axis="y", useOffset=False, useMathText=False)
# Save the figure as a PNG file
plt.tight_layout()
plt.savefig("pareto.png", dpi=300)
