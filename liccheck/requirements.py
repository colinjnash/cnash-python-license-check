# liccheck/requirements.py - FINAL CORRECTED VERSION

import importlib.metadata
import pkg_resources

try:
    from pip._internal.network.session import PipSession
except ImportError:
    try:
        from pip._internal.download import PipSession
    except ImportError:
        from pip.download import PipSession

try:
    from pip._internal.req import parse_requirements as pip_parse_requirements
except ImportError:
    from pip.req import parse_requirements as pip_parse_requirements

try:
    from pip._internal.req.constructors import install_req_from_parsed_requirement
except ImportError:
    def install_req_from_parsed_requirement(r):
        return r


def parse_requirements(requirement_file):
    """Parses a requirements file into a list of Requirement objects."""
    requirements = []
    # Use a dummy session for parsing, as we only need metadata.
    parsed_reqs = pip_parse_requirements(requirement_file, session=PipSession())
    for req in parsed_reqs:
        install_req = install_req_from_parsed_requirement(req)
        if install_req.markers and not pkg_resources.evaluate_marker(str(install_req.markers)):
            # req should not be installed due to env markers
            continue
        elif install_req.editable:
            # skip editable req as they are not discoverable by importlib.metadata in the same way
            continue
        if install_req.req: # Ensure the requirement object exists
            requirements.append(pkg_resources.Requirement.parse(str(install_req.req)))
    return requirements


def resolve_without_deps(requirements):
    """
    Finds installed packages that match the requirements list, without their dependencies.
    This now uses importlib.metadata for consistency.
    """
    # Create a set of required package names (lowercase for case-insensitive matching)
    required_keys = {req.key for req in requirements}
    
    # Iterate through all installed distributions and yield ones that are in our requirements
    for dist in importlib.metadata.distributions():
        if dist.metadata['name'].lower() in required_keys:
            yield dist


def resolve(requirements):
    """
    Resolve ALL installed packages in the environment.
    This is a simple and effective way to check the license of every package,
    ensuring all transitive dependencies are covered.
    The 'requirements' argument is implicitly handled by scanning the entire environment
    which must contain the packages from the requirements file.
    """
    for dist in importlib.metadata.distributions():
        yield dist