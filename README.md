# Airflow Workbook

A hands-on guide to running Apache Airflow locally on **macOS**. This workbook covers setup, essential commands, and best practices for developing and debugging DAGs. (Not tested on Windows.)

---

## Table of Contents
- [Requirements](#requirements)
- [Setting Up Environment](#setting-up-environment)
- [Activating Your Environment](#activating-your-environment)
- [Airflow Commands](#airflow-commands)
- [Other Useful Commands](#other-useful-commands)
- [How to Airflow: Step-by-Step](#how-to-airflow-step-by-step)
- [DAG Examples](#dag-examples)

---

## Requirements
- **Python 3.11** (required for Apache Airflow 2.10.5)
- **Poetry** (for dependency management)

---

## Setting Up Environment
1. Configure Poetry to use in-project virtual environments:
   ```sh
   poetry config virtualenvs.in-project true
   ```
2. Lock dependencies:
   ```sh
   poetry lock
   ```

**Debugging Python version issues:**
- If you get a "python version not found" error:
  ```sh
  brew install python@3.11
  poetry env list
  poetry env remove <values that are returned>
  # Ensure no environments remain by poetry env list, then:
  poetry lock
  poetry install
  ```
- You should see a `.venv` directory appear if your environment is set up correctly.

---

## Activating Your Environment
- Try running:
  ```airflow --version```
- If this fails, it's because your terminal hasn't activated the Poetry environment where Airflow was installed.

**To activate:**
```source .venv/bin/activate ```
- Now, check Airflow:
  ```airflow --version ```
- To confirm dependencies:
  ```poetry show```
  (Look for `apache-airflow` and related packages.)

**Extra:**
- Why does `poetry run airflow --version` work even if you don't activate the environment? 

---

## Airflow Commands

### Environment Variables
- Set Airflow home and DAGs folder:
  ```zsh
  export AIRFLOW_HOME=$(pwd)/
  export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/{relative dag path}
  # Example:
  export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/dags/nested_dags/dags/another_folder
  ```

### Core Commands
- **Initialize the database:**
  ```airflow db init```
- **Create an admin user:**
  ``` airflow users create --role Admin --username <YOUR_USERNAME> --email <YOUR_EMAIL> --firstname <YOUR_FIRSTNAME> --lastname <YOUR_LASTNAME> --password <YOUR_PASSWORD> ```
- **Start the webserver:**
  ```airflow webserver```
- **Start the scheduler:**
  ```airflow scheduler```

---

## Other Useful Commands
- **Stop all Airflow processes:**
  ```sh
  pkill -f airflow
  # (Use when you want to restart everything or are mad at airflow)
  ```
- **Show which Airflow is running:**
  ```sh
  which airflow
  ```
- **Disable example DAGs:**
  ```sh
  sed -i '' 's/^load_examples *= *.*/load_examples = False/' airflow.cfg
  ```
- **Print Airflow home directory:**
  ```sh
  echo $AIRFLOW_HOME
  ```

---

## How to Airflow: Step-by-Step

### 1. Initialize and Create User
```sh
airflow db init
airflow users create --role Admin --username <YOUR_USERNAME> --email <YOUR_EMAIL> --firstname <YOUR_FIRSTNAME> --lastname <YOUR_LASTNAME> --password <YOUR_PASSWORD>
```

### 2. Start Services
- In one terminal:
  ```sh
  export AIRFLOW_HOME=$(pwd)/
  airflow webserver
  ```
- In another terminal:
  ```sh
  export AIRFLOW_HOME=$(pwd)/
  airflow scheduler
  ```

### 3. Access the UI
- Look for `Listening at:` in the webserver terminal (usually http://0.0.0.0:8080)
- Sign in and run your DAGs.

### 4. Debugging
- Check logs to ensure your tasks are running as expected.
- To restart everything, run:
  ```sh
  pkill -f airflow
  # Then restart webserver and scheduler as above
  ```

---

## DAG Examples

### TaskFlow API Example (`dags/nested_dags/task_decorator.py`)
- The recommended, cleanest way to define tasks in Airflow.
- Keeps business logic separate from DAG structure.

**Challenge:** Try to rewrite the DAG so that the total is 21!

### PythonOperator Example (`dags/nested_dags/python_operator.py`)
- Same logic as above, but more verbose.
- Sometimes useful for ETL pipelines where each step is a distinct task.

---

## Best Practices
- Use the TaskFlow API (`@task`) for new DAGs.
- Keep core logic in separate scripts (not in `dags/`), and adjust `sys.path` if needed to avoid relative imports.
- Restart Airflow processes after making changes to DAGs or dependencies.

---

Happy Airflowing! 🚀
