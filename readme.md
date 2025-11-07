# `liccheck` (v4.0.0)

A tool to check the licenses of your Python dependencies against a defined strategy.

This is a modernized fork of the original `dhatim/python-license-check` tool, updated with `pyproject.toml` support, improved dependency resolution using `importlib.metadata`, and a more robust license detection strategy.

## Key Features

- **Modern Configuration:** Configure the tool directly in your `pyproject.toml` under the `[tool.liccheck]` section. Legacy `liccheck.ini` files are still supported.
- **`pyproject.toml` Dependency Source:** Automatically find and check dependencies from your `[project.dependencies]` or `[tool.poetry.dependencies]` sections, including optional dependency groups.
- **Improved License Detection:** Uses a more reliable 4-step process to find a package's license:
  1.  Reads `License-Expression` or `License` from package metadata.
  2.  Fetches license info from the **PyPI JSON API** as a fallback.
  3.  Checks `Classifier` metadata.
  4.  Reads common `LICENSE` files (`LICENSE`, `LICENSE.MD`, `COPYING`, etc.) as a last resort.
- **Full Environment Scanning:** By default, `liccheck` now scans your _entire_ Python environment to find all installed packages and their transitive dependencies, ensuring nothing is missed. You can revert to the old behavior (`--no-deps`) to check only top-level packages.
- **Better Dependency Reporting:** Use the `--dep-depth` flag to control how dependency trees are printed for packages with problematic licenses.

## Installation

```bash
# Install from source
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
pip install .

# Or install directly from your Git repository
pip install git+[https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
```

## Usage

`liccheck` works by comparing your installed packages against a "strategy" that defines authorized and unauthorized licenses.

### 1\. Configure Your Strategy

You can configure `liccheck` in two ways. Using `pyproject.toml` is recommended.

#### Recommended: `pyproject.toml`

Add a `[tool.liccheck]` section to your `pyproject.toml` file. `liccheck` will automatically find and use this configuration.

```toml

[tool.liccheck]
# --- Dependency Source ---
# Automatically find dependencies from this pyproject.toml
dependencies = true
# Optionally include dependency groups (e.g., [project.optional-dependencies])
# Use ["*"] to check all optional dependencies
optional_dependencies = ["dev", "test"]

# (Alternative) If not using the settings above, specify a requirements file
# requirement_txt_file = "requirements.txt"

# --- Check Strategy ---
# One of: STANDARD, CAUTIOUS, PARANOID (see "Compliance Levels" below)
level = "CAUTIOUS"

# Enable regex matching for license names
as_regex = false

# How to display dependency trees for failures
# 0 = no dependencies, 1 = direct parents, -1 = full tree
dep_depth = 1

# --- License Lists ---
authorized_licenses = [
    "MIT",
    "Apache-2.0",
    "BSD-3-Clause",
    "ISC",
]

unauthorized_licenses = [
    "GPL.*", # Requires as_regex = true
    "AGPL-3.0-only",
]

# --- Package-Specific Overrides ---
[tool.liccheck.authorized_packages]
# Always allow "my-internal-package" regardless of its license
"my-internal-package" = "*"

# Only allow "package-name" if it matches the version spec
"package-name" = ">=1.0,<2.0"

```

#### Legacy: `liccheck.ini`

You can also use a traditional `liccheck.ini` file and pass it via the command line.

```ini
[Licenses]
authorized_licenses =
    MIT
    Apache-2.0
    BSD-3-Clause
    ISC
unauthorized_licenses =
    AGPL-3.0-only

[Authorized Packages]
my-internal-package = *
package-name = >=1.0,<2.0
```

### 2\. Run the Check

If you configured `liccheck` using `pyproject.toml`, just run the command:

```bash
liccheck
```

If you are using a legacy `.ini` file or a `requirements.txt` file, specify them:

```bash
liccheck --sfile liccheck.ini --rfile requirements.txt
```

#### Example Output

```
liccheck version 4.0.0
gathering licenses...
212 packages and dependencies.
check authorized packages...
209 packages.
check unauthorized packages...
1 packages.
    problem-package (1.2.3): ['AGPL-3.0-only']
      dependencies:
          my-project
check unknown packages...
2 packages.
    unknown-package (0.1.0): []
      dependencies:
          dependency-of-mine
    other-package (3.3.0): ['UNKNOWN']
      dependencies:
          my-project
```

The script will exit with a non-zero status code if unauthorized or unknown licenses are found.

## Command-Line Options

| Argument            | `pyproject.toml` Key   | Description                                                                                                        |
| :------------------ | :--------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `-s`, `--sfile`     | `strategy_ini_file`    | Path to your strategy `.ini` file. (Not needed if using `pyproject.toml`).                                         |
| `-r`, `--rfile`     | `requirement_txt_file` | Path to your `requirements.txt` file. (Not needed if using `[tool.liccheck].dependencies`).                        |
| `-l`, `--level`     | `level`                | Compliance level: `STANDARD`, `CAUTIOUS`, or `PARANOID`.                                                           |
| `--no-deps`         | `no_deps`              | Only check packages listed in the requirements file; do not scan the full environment for transitive dependencies. |
| `--as-regex`        | `as_regex`             | Enable regex matching for license names in your strategy.                                                          |
| `--dep-depth`       | `dep_depth`            | Set dependency printout depth: `0` (none), `1` (direct, default), `-1` (full tree).                                |
| `-R`, `--reporting` | `reporting_txt_file`   | Path to an output file for a simple report (e.g., `package version license status`).                               |
| `-v`, `--version`   | N/A                    | Show the program's version number and exit.                                                                        |

## Compliance Levels

You can set the strictness of the check using the `--level` (or `level` key):

- **`STANDARD`** (Default): Fails if a package has **no** authorized licenses. It passes if _at least one_ license is authorized, even if others are not.
- **`CAUTIOUS`**: Fails if a package has **no** authorized licenses OR if it has _any_ unauthorized licenses.
- **`PARANOID`**: Fails unless **all** of a package's licenses are authorized.

## License

This project is licensed under the Apache Software License.

```

```
