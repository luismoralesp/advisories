# Advisories

## Project Description

Advisories is a script that downloads all GitHub security vulnerabilities from the [GitHub Advisory Database](https://github.com/advisories). It then zips up the advisories by severity, creating 4 zip files for each severity category: low, moderate, high, and critical.

Aditionally this feature includes the ability to generate a CSV file that lists every vulnerability, with each row containing key attributes summarizing important details. Additionally, the CSV file includes a KEV field. If a vulnerability is listed in the C[ISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog), the KEV field is populated with a value of 1; otherwise, the field is left empty

## Installation

Follow these steps to install the project:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/luismoralesp/advisories
    cd advisories
    ```

2. **Create and activate a virtual environment (optional but recommended)**:
    ```bash
    virtualenv env --python=python3
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
*How to install virtual env [see](https://virtualenv.pypa.io/en/latest/installation.html)*

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To execute the application, simply run the `main.py` file located in the root directory of the project:

```bash
python main.py
```

## Running the Tests

To run the project's tests, follow these steps:

1. **Ensure all dependencies are installed**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the tests**:
    ```bash
    python -m unittest
    ```

## Python Version

This project has been tested with Python 3.12.3. Make sure you are using a compatible version of Python to avoid compatibility issues.

## Diagrams

### General Project Diagram

![General Diagram](diagrams/diagram.jpeg)

### Class Diagram

![Class Diagram](diagrams/class-diagram.jpeg)

## How to Contribute

Contributions are welcome and appreciated. To contribute to the project:

1. **Fork** the repository.
2. Create a new **branch** for your feature or fix:
    ```bash
    git checkout -b feature/new-feature
    ```
3. Make your changes and ensure all tests pass.
4. **Commit** your changes:
    ```bash
    git commit -m "Add new feature"
    ```
5. **Push** to the branch:
    ```bash
    git push origin feature/new-feature
    ```
6. Create a **Pull Request** on GitHub.

Please make sure to follow the project's guidelines and maintain code consistency.

---

Thank you for contributing and for using RepoClonerHandler. We hope this tool is helpful to you!
