# How to run unit tests of group 6 🏃

- [How to run unit tests of group 6 🏃](#how-to-run-unit-tests-of-group-6-)
  - [Prerequisites 🔩](#prerequisites-)
  - [Setup 🔧](#setup-)
  - [Run test 👟](#run-test-)
  - [Afterwords 📃](#afterwords-)

## Prerequisites 🔩
- You know how to run the backend server of this project

## Setup 🔧
- First, we need to create the tasks in database. 
  - Run the server (the run-server one, not the test one) and turn on the database.
  - Clear the database by using run-seed-db.
  - Open a new terminal, change your working directory to this directory (containing this README.md).
  - If you want to, you can create new test cases by running the following command (the default seed is 31415):
  ```
    python3 testcase_generator.py [seed]
  ```
  - Next, run the following command to create the tasks in database:
  ```
    python3 task_generator.py
  ```
  - The running process might take a while (depending on the number of test cases), you can delete some testcases if you like.
  - Ignore the `failed to translate` message, it is normal since the translator can't translate those testcases.
  - Finally, you need to add the job to */background_tasks/main.py*.

## Run test 👟
- After finishing the setup above, you can test this module just like how you test the other modules.

## Afterwords 📃
- After running the tests, we can see that almost every failed testcases are due to the translator can't translate those testcases (unknown language or non human readable).

