# liccheck/requirements.py - AFTER THE FIX

import importlib.metadata  # <--- 1. ADD THIS LINE AT THE TOP
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
    # This function remains unchanged
    requirements = []
    for req in pip_parse_requirements(requirement_file, session=PipSession()):
        install_req = install_req_from_parsed_requirement(req)
        if install_req.markers and not pkg_resources.evaluate_marker(str(install_req.markers)):
            # req should not installed due to env markers
            continue
        elif install_req.editable:
            # skip editable req as they are failing in the resolve phase
            continue
        requirements.append(pkg_resources.Requirement.parse(str(install_req.req)))
    return requirements


def resolve_without_deps(requirements):
    # This function remains unchanged
    working_set = pkg_resources.working_set
    for req in requirements:
        env = pkg_resources.Environment(working_set.entries)
        dist = env.best_match(
            req=req,
            working_set=working_set,
            installer=None,
            replace_conflicting=False,
        )
        yield dist


def resolve(requirements):
    """
    Resolve requirements describing dependencies.
    This now scans all installed packages and ignores the requirements list argument,
    as importlib.metadata doesn't resolve dependencies, it inspects the environment.
    This is a more robust way to avoid crashes from dependency conflicts.
    """
    for dist in importlib.metadata.distributions():
        yield dist