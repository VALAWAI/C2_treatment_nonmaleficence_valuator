# C2_treatment_nonmaleficence_valuator

The C2 treatment non-maleficence valuator obtains the non-maleficence value after applying a treatment to a patient.

## Summary

- **Type**: [C2](https://valawai.github.io/docs/components/C2/)
- **Name**: Treatment nonmaleficence valuator
- **Documentation**: [https://valawai.github.io/docs/components/C2/treatment_nonmaleficence_valuator](https://valawai.github.io/docs/components/C2/treatment_nonmaleficence_valuator)
- **Versions**:
  - **Stable version**: [1.1.0 (February 23, 2026)](https://github.com/VALAWAI/C2_treatment_nonmaleficence_valuator/tree/1.1.0)
  - **API**: [1.0.2 (April 30, 2025)](https://raw.githubusercontent.com/VALAWAI/C2_treatment_nonmaleficence_valuator/ASYNCAPI_1.0.2/asyncapi.yaml)
  - **Required MOV API**: [1.2.0 (March 9, 2024)](https://raw.githubusercontent.com/valawai/MOV/ASYNCAPI_1.2.0/asyncapi.yml)
- **Developed By**: [IIIA-CSIC](https://www.iiia.csic.es)
- **License**: [GPL v3](LICENSE)
- **Technology Readiness Level (TLR)**: [3](https://valawai.github.io/docs/components/C2/treatment_nonmaleficence_valuator/tlr)

## Usage

The Treatment Non-maleficence Valuator (C2) serves as a specialized evaluation engine designed to measure how effectively a proposed dental treatment adheres to the fundamental medical principle of "first, do no harm." By processing specific data regarding the intended clinical treatment alongside
the current physiological vulnerabilities of the patient, the component analyzes the decision-making
framework to ensure that the risks of the procedure do not outweigh the potential benefits. Once this
data is processed, the component generates an automated feedback score within a precise range of -1
to 1, where a value of -1 indicates a significant risk of avoidable harm or complications, and a
value of 1 represents complete alignment with protective safety standards. This allows practitioners
to instantly identify whether a digital treatment plan minimizes clinical risk or if it requires
further manual adjustment to ensure the patient’s safety and physical integrity are fully preserved.

## Deployment

The **C2 Treatment nonmaleficence valuator** is designed to run as a Docker container, working within
the [Master Of VALAWAI (MOV)](https://valawai.github.io/docs/architecture/implementations/mov) ecosystem.
For a complete guide, including advanced setups, refer to
the [component's full deployment documentation](https://valawai.github.io/docs/components/C2/treatment_nonmaleficence_valuator/deploy).

Here's how to quickly get it running:

1. ### Build the Docker Image

   First, you need to build the Docker image. Go to the project's root directory and run:

   ```bash
   ./buildDockerImages.sh -t latest
   ```

   This creates the `valawai/c2_treatment_nonmaleficence_valuator:latest` Docker image, which is referenced in the `docker-compose.yml` file.

2. ### Start the Component

   You have two main ways to start the component:

   A. **With MOV:**
   To run the C2 Treatment nonmaleficence valuator with the MOV, use:

   ```bash
   COMPOSE_PROFILES=all docker compose up -d
   ```

   Once started, you can access:
   - **MOV:** [http://localhost:8081](http://localhost:8081)
   - **RabbitMQ UI:** [http://localhost:8082](http://localhost:8082) (credentials: `mov:password`)
   - **Mongo DB:** `localhost:27017` (credentials: `mov:password`)

   B. **As a Standalone Component (connecting to an existing MOV/RabbitMQ):**
   If you already have MOV running or want to connect to a remote RabbitMQ, you'll need a
   [`.env` file](https://docs.docker.com/compose/environment-variables/env-file/) with connection
   details. Create a `.env` file in the same directory as your `docker-compose.yml` like this:

   ```properties
   MOV_MQ_HOST=host.docker.internal
   MOV_MQ_USERNAME=mov
   MOV_MQ_PASSWORD=password
   ```

   Find full details on these and other variables in the
   [component's dedicated deployment documentation](https://valawai.github.io/docs/components/C2/treatment_nonmaleficence_valuator/deploy).
   Once your `.env` file is configured, start only the component (without MOV) using:

   ```bash
   COMPOSE_PROFILES=component docker compose up -d
   ```

3. ### Stop All Containers

   To stop all containers launched, run:

   ```bash
   COMPOSE_PROFILES=all docker compose down
   ```

   This command stops the MOV and RabbitMQ containers.

## Development environment

To ensure a consistent and isolated development experience, this component is configured
to use Docker. This approach creates a self-contained environment with all the necessary
software and tools for building and testing, minimizing conflicts with your local system
and ensuring reproducible results.

You can launch the development environment by running this script:

```bash
./startDevelopmentEnvironment.sh
```

Once the environment starts, you'll find yourself in a bash shell, ready to interact with
the necessary tools for the component's development in Python. You'll also have access
to the following integrated tools:

- **Master of VALAWAI**: The central component managing topology connections between services.
  Its web interface is accessible at [http://localhost:8081](http://localhost:8081).
- **RabbitMQ** The message broker for inter-component communication. The management web interface
  is at [http://localhost:8082](http://localhost:8082), with credentials `mov:password`.
- **MongoDB**: The database used by the MOV, named `movDB`, with user credentials `mov:password`.
- **Mongo express**: A web interface for interacting with MongoDB, available at
  [http://localhost:8084](http://localhost:8084), also with credentials `mov:password`.

Within this console, you can use the next commands:

- **run:** Starts the C2 Treatment nonmaleficence valuator component.
- **testAll:** Runs all unit tests for the codebase.
- **test test/test_something.py:** Runs the unit tests defined in
  the file `test_something.py`.
- **test test/test_something.py::TestClassName::test_do_something:** Runs
  a specific unit test named `test_do_something` defined within the class `TestClassName`
  in the file `test_something.py`.
- **coverage:** Runs all unit tests and generates a coverage report.
- **fmt:** Runs a static code analyzer to check for formatting and style issues.

To exit the development environment, simply type `exit` in the bash shell or run the following script:

```bash
./stopDevelopmentEnvironment.sh
```

In either case, the development environment will gracefully shut down, including all activated services like MOV, RabbitMQ, MongoDB, and Mongo Express.

## Helpful Links

Here's a collection of useful links related to this component and the VALAWAI ecosystem:

- **C2 Treatment nonmaleficence valuator Documentation**: [https://valawai.github.io/docs/components/C2/treatment_nonmaleficence_valuator](https://valawai.github.io/docs/components/C2/treatment_nonmaleficence_valuator)
- **Master Of VALAWAI (MOV)**: [https://valawai.github.io/docs/architecture/implementations/mov/](https://valawai.github.io/docs/architecture/implementations/mov/)
- **VALAWAI Main Documentation**: [https://valawai.github.io/docs/](https://valawai.github.io/docs/)
- **VALAWAI on GitHub**: [https://github.com/VALAWAI](https://github.com/VALAWAI)
- **VALAWAI Official Website**: [https://valawai.eu/](https://valawai.eu/)
- **VALAWAI on X (formerly Twitter)**: [https://x.com/ValawaiEU](https://x.com/ValawaiEU)
