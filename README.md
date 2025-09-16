# Enhanced Python License Checker

This tool is a heavily modified and enhanced version of the original [license-check](https://www.google.com/search?q=https://github.com/dameon/license-check) utility by Dameon Rogers.

It is designed to be integrated into a CI/CD pipeline to automatically verify that all Python package dependencies (including transitive dependencies) comply with a predefined set of open-source licenses. If a non-compliant, unapproved, or unknown license is found, the script will exit with a non-zero status code, failing the build.

The key enhancements in this version focus on robust, multi-layered automatic license detection to eliminate the need for manual overrides for public packages.

## Features

  * **Robust 4-Step License Detection:** The script uses a sophisticated, prioritized hierarchy to find the license for each package, ensuring maximum accuracy:
    1.  Checks for modern `License-Expression` metadata.
    2.  Falls back to the legacy `License` metadata field.
    3.  If no local metadata is found, it queries the official **PyPI JSON API** for the authoritative license.
    4.  As a last resort, it reads and parses local `LICENSE` text files.
  * **Configurable Package Authorization:** Use the configuration file to approve internal/proprietary packages that are not on public registries.
  * **Configurable Dependency Reporting:** Control the verbosity of dependency printouts for failing packages using the `--dep-depth` argument, keeping CI logs clean and readable.
  * **INI-Based Configuration:** Manage your list of approved licenses and authorized packages in a simple and clear `.ini` file.

## Installation

Use these instructions to add the script to your project.

1.  Place the `liccheck` directory (containing our modified `command_line.py` and `requirements.py`) into your project's repository.
2.  Make the script entry point executable (if required by your system).
3.  Install the script's dependencies.
    ```sh
    pip install semantic-version toml
    ```

## Configuration

Control the behavior of the checker by creating a `license_check.ini` file in the root of your project.

### Example `license_check.ini`

```ini
[Licenses]
# List all license names that are approved for use in your project.
# The check is case-insensitive.
authorized_licenses:
    mit
    apache-2.0
    bsd-3-clause
    bsd-2-clause
    isc
    psf-2.0
    mpl-2.0

[Authorized Packages]
# This section is for authorizing packages by name.
# This is primarily for internal/proprietary packages that are not on PyPI.
# The '*' means any version of the package is authorized.
my-internal-package: *
another-proprietary-lib: *

[Unauthorized Licenses]
# You can explicitly fail the build if certain licenses are found.
# For example, to forbid the GPL license:
# unauthorized_licenses:
#     gpl
```

## Usage

Run the script from the command line, pointing it to your strategy (`.ini`) file and your requirements file.

```sh
# Generate a requirements file from your current environment
pip freeze > requirements.txt

# Run the check
liccheck -s license_check.ini -r requirements.txt
```

### Command-Line Arguments

The script's behavior can be modified with the following arguments:

| Argument | Short | Description |
| :--- | :--- | :--- |
| `--version` | `-v` | Show the script's version number and exit. |
| `--sfile <file>` | `-s` | Path to the strategy `.ini` file. Defaults to `./liccheck.ini`. |
| `--rfile <file>` | `-r` | Path to the `requirements.txt` file. Defaults to `./requirements.txt`. |
| `--level <level>` | `-l` | Set the compliance level (`STANDARD`, `CAUTIOUS`, `PARANOID`). Defaults to `STANDARD`. |
| `--reporting <file>` | `-R` | Write a detailed report of all packages and their status to the specified file. |
| `--dep-depth <int>` | | Set dependency printout depth for failing packages. `0`=none, `1`=direct (default), `-1`=full. |
| `--no-deps` | | Do not check transitive dependencies. |
| `--as-regex` | | Treat license names in the `.ini` file as regular expressions. |

## CI/CD Integration Example

This tool is ideal for a quality gate in your CI/CD pipeline. Here is a sample job for GitLab CI:

```yaml
license_check:
  stage: test
  image: python:3.11
  script:
    # Install the tool's dependencies
    - pip install semantic-version toml

    # Install your project's dependencies
    - pip install -r requirements.txt

    # Generate a complete list of all installed packages
    - pip freeze > liccheck-requirements.txt

    # Run the license check and generate a report artifact
    - liccheck -s license_check.ini -r liccheck-requirements.txt -R os-licenses.txt
  artifacts:
    when: always
    paths:
      - os-licenses.txt
```

## Omissions

  * This tool is not a substitute for legal advice. Its purpose is to automate checks against a pre-approved list, not to interpret the legal meaning of a license.
  * The script cannot analyze the licenses of non-Python dependencies (e.g., system libraries, C/C++ extensions).
  * The automatic detection is based on metadata and heuristics. While robust, it may fail on obscure or poorly packaged libraries.

License

This modified script is licensed under the Apache License 2.0, inheriting from the original project.

## Acknowledgements

This tool is based on and heavily adapted from the original `license-check` project created by Dameon Rogers.