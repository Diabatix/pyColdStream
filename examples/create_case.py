# -------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#                                    EXAMPLE
#
#
# -------------------------------------------------------------------------------#

from coldstream import ColdstreamSession, case
import os


# ======================= SESSION AND PROJECT FUNCTIONS ======================= #

def create_session():
    """Create and return a ColdStream session."""
    return ColdstreamSession.create_from_login(user="maarten.haine@diabatix.com",
                                               password="msY#xJ!t#gig4heq",
                                               host="stage.helios")


def create_project_and_case(session):
    """Create a project and case, returning the case object."""
    project = session.projects.create_project("Example Project",
                                              "This is an example project, with a template case.")
    case_obj1 = project.create_case(case.Case.CASE_TYPES["Simulation"], "Example Case 1")
    case_obj2 = project.create_case(case.Case.CASE_TYPES["Simulation"], "Example Case 2")
    return case_obj1, case_obj2


# ======================= OPTION 1: COMPOUND GEOMETRY ======================= #
"""
Option 1: Upload a compound STEP file with all regions, subregions and boundaries 
pre-defined in a single file..
"""


def create_complete_case(case_obj):
    """Upload a compound STEP file containing all geometries at once."""
    geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'Compound_V2.stp')
    case_obj.upload_geometry_file(geometry_file_path)
    return case_obj


def get_components_complete_case(case_obj):
    """Extract all regions, subregions, and boundaries from a compound case."""
    regions_dict = {}
    for region in case_obj.regions:
        subregions_dict = {}
        for subregion in region.subregions:
            subregions_dict[subregion.ID] = {
                "subregion": subregion.data['name'],
            }
        regions_dict[region.ID] = {
            "region": region.data['name'],
            "subregions": subregions_dict,
            "boundaries": {boundary.ID: boundary.data['name'] for boundary in region.boundaries}
        }
    return regions_dict


# ====================== OPTION 2: INDIVIDUAL COMPONENTS ====================== #
"""
Option 2: Add each component (regions, subregions, boundaries) separately.
"""


def add_first_region(case_obj):
    """Add the first region (Housing) to the case."""
    reg1 = case_obj.create_region('region1')
    geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'solid426161.step')
    reg1.upload_geometry_file(geometry_file_path)
    data = {
        "physics": {
            "properties": {
                "id": 631,
                "name": "ST Collector solid",
                "rho": 8000,
                "Cp": 4500,
                "kappa": 80
            },
            "radiation": {
                "radiation": "disabled"
            }
        },
        "sources": {
            "power": {
                "properties": {
                    "Q": 25
                }
            }
        }
    }
    reg1.update("Housing", "solid", data)
    return reg1


def add_second_region(case_obj):
    """Add the second region (Fluid) to the case."""
    reg2 = case_obj.create_region('region2')
    geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'fluid426160.step')
    reg2.upload_geometry_file(geometry_file_path)
    data = {
        "physics": {
            "properties": {
                "id": 1418,
                "name": "ST Collector fluid",
                "rho": 1000,
                "mu": 0.000959,
                "Cp": 4181,
                "kappa": 0.60567
            },
            "buoyancy": {
                "buoyancy": "disabled",
                "pref": 101325,
                "Tref": 293.15,
                "g": []
            },
            "radiation": {
                "radiation": "disabled"
            },
            "turbulence": "kOmegaSST"
        }
    }
    reg2.update("Fluid", "fluid", data)
    return reg2


def add_boundaries_and_subregion(reg2):
    """Add boundaries and subregion to the second region."""
    # Add subregion
    subreg1 = reg2.create_subregion("subreg1")
    geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'standardDesign426163.step')
    subreg1.upload_geometry_file(geometry_file_path)
    data = {
        "sources": {},
        "physics": {
            "properties": {
                "id": 525,
                "name": "ST Collector design",
                "rho": 8000,
                "Cp": 450,
                "kappa": 80
            }
        }
    }
    subreg1.update("Design", "design", data)

    # Add inlet boundary
    bound1 = reg2.create_boundary("boundary1")
    geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'fixedFlowRateInlet426146.step')
    bound1.upload_geometry_file(geometry_file_path)
    data = {
        "properties": {
            "T": 293.15,
            "U": 4
        }
    }
    bound1.update("Inlet", "fixedFlowRateInlet", data)

    # Add outlet boundary
    bound2 = reg2.create_boundary("boundary2")
    geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'pressureOutlet426147.step')
    bound2.upload_geometry_file(geometry_file_path)
    data = {
        "properties": {
            "p": 2500
        }
    }
    bound2.update("Outlet", "pressureOutlet", data)

    return bound2


def add_target(case_obj, boundary):
    """Add target to the case using the specified boundary."""
    target = case_obj.create_target(boundary.ID)
    data = {
        "constraintType": "velocityVariance",
        "target": 100
    }
    target.update("constraint", data)
    return target


def add_third_region(case_obj):
    """Add the third region (Heatsources) to the case."""
    reg3 = case_obj.create_region('region3')
    geometry_file_path = os.path.join(os.path.dirname(__file__), 'step_files', 'solid426162.step')
    reg3.upload_geometry_file(geometry_file_path)
    data = {
        "physics": {
            "properties": {
                "id": 631,
                "name": "ST Collector solid",
                "rho": 8000,
                "Cp": 4500,
                "kappa": 80
            },
            "radiation": {
                "radiation": "disabled"
            }
        },
        "sources": {
            "power": {
                "properties": {
                    "Q": 25
                }
            }
        }
    }
    reg3.update("Heatsources", "solid", data)
    return reg3


# ============================= MAIN FUNCTION ============================= #

def main():
    """Main function to execute the ColdStream case creation workflow."""
    # ---------------- INITIALIZE SESSION ---------------- #
    print('Initializing ColdStream session...')
    session = create_session()

    # ---------------- CREATING CASES ---------------- #
    print('Creating project and cases...')
    case_obj1, case_obj2 = create_project_and_case(session)
    print(f'Cases created successfully: {case_obj1.ID} and {case_obj2.ID}')
    print('=====================================================')

    # ================== OPTION 1 EXECUTION ================== #
    print('EXECUTING OPTION 1: COMPOUND GEOMETRY APPROACH')
    print('------------------------------------------------')

    print('Uploading compound STEP file...')
    create_complete_case(case_obj1)
    print('Compound file uploaded successfully')
    print('=====================================================')

    # ================== OPTION 2 EXECUTION ================== #
    print('EXECUTING OPTION 2: COMPONENT-BY-COMPONENT APPROACH')
    print('---------------------------------------------------')

    print('Adding first region (Housing)...')
    add_first_region(case_obj2)
    print('First region added successfully')
    print('-------------------------------------')

    print('Adding second region (Fluid)...')
    reg2 = add_second_region(case_obj2)
    print('Second region added successfully')
    print('-------------------------------------')

    print('Adding boundaries and subregion to second region...')
    outlet_boundary = add_boundaries_and_subregion(reg2)
    print('Boundaries and subregion added successfully')
    print('-------------------------------------')

    print('Adding target to case...')
    add_target(case_obj2, outlet_boundary)
    print('Target added successfully')
    print('-------------------------------------')

    print('Adding third region (Heatsources)...')
    add_third_region(case_obj2)
    print('Third region added successfully')
    print('=====================================================')

    # ---------------- COMPLETION SUMMARY ---------------- #
    print('CASE CREATION COMPLETED SUCCESSFULLY')
    print(f'Option 1 Case ID: {case_obj1.ID}')
    print(f'Option 2 Case ID: {case_obj2.ID}')


if __name__ == "__main__":
    main()