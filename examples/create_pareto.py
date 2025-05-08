# -------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#                                    EXAMPLE
#
#
# -------------------------------------------------------------------------------#

import matplotlib.pyplot as plt
from pycoldstreamv0_3.coldstream import ColdstreamSession


def create_session():
    """Create and return a ColdStream session."""
    return ColdstreamSession.create_from_login(user="admin@admin.com",
                                               password="admin",
                                               host="eu1")


def get_project_and_case(session, project_id, case_id):
    """Retrieve project and case objects using their IDs."""
    project = session.projects.get_project(project_id)
    case = project.get_case(case_id)
    return project, case


def extract_plot_data(case):
    """Extract x and y data for the plot from case results."""
    # Extract x data from pressure loss target
    x_data = None
    for target in case.get_results_evolution_graph().data["targetGraphs"]:
        if target["targetType"] == "pressureLoss":
            x_data = [t_i["value"] for t_i in target["results"]]
            break

    # Extract y data from overall design performance
    y_data = [r_i["value"] for r_i in
              case.get_results_evolution_graph().data["overallDesignPerformanceGraph"]["results"]]

    return x_data, y_data


def create_pareto_plot(x_data, y_data, output_filename="pareto.png"):
    """Create and save a pareto plot with the provided data."""
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, marker='+', linestyle='', label="title pareto")

    # Add grid and legend
    plt.grid(True)
    plt.legend()
    plt.xlabel(r"$\Delta P$")
    plt.ylabel(r"$J$")

    # Configure formatting
    plt.ticklabel_format(style="plain", axis="y", useOffset=False, useMathText=False)

    # Save the figure
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)

    return output_filename


def main():
    """Main function to execute the ColdStream data plotting workflow."""
    # ---------------- INITIALIZE SESSION ---------------- #
    print('Initializing ColdStream session...')
    session = create_session()

    # ---------------- RETRIEVING PROJECT AND CASE ---------------- #
    project_id = 1550 # Example project ID
    case_id = 5429 # Example case ID
    print(f'Retrieving project ID {project_id} and case ID {case_id}...')
    project, case = get_project_and_case(session, project_id, case_id)
    print('Project and case retrieved successfully')
    print('=====================================================')

    # ---------------- EXTRACTING PLOT DATA ---------------- #
    print('Extracting plot data from case results...')
    x_data, y_data = extract_plot_data(case)
    if x_data is None:
        print('Error: Could not find pressure loss target data')
        return
    print(f'Data extracted successfully: {len(x_data)} data points')
    print('=====================================================')

    # ---------------- CREATING PARETO PLOT ---------------- #
    print('Creating pareto plot...')
    output_file = create_pareto_plot(x_data, y_data)
    print(f'Plot saved successfully as {output_file}')
    print('=====================================================')

    # ---------------- PROCESS COMPLETED ---------------- #
    print('Data visualization process completed successfully')


if __name__ == "__main__":
    main()