# Displaying Turing Machines

The goal of this lab is to implement a visual interface for our Turing Machine simulator.

After finishing, we would like to be able to call something like this:

```bash
python yatumas.py -m examples/add_one.tm -i 0.3 10111
```

This should run a machine from file `examples/add_one.tm` with interval between steps set to `0.3`s on input `10111`.

![](result.mp4)

## TODO: 

There are several tasks to complete:
- [ ] make sure, you have a proper working environment, install the reuirementes via `pip`. More in section: `Preparations`
- [ ] finish up the Model-View-Controller architecture of our visualisation:
    - [ ] model: `yatumas/simulator/model.py`
    - [ ] controller: `yatumas/simulator/controller.py`
    - [ ] view `yatumas/simulator/view.py`
- [ ] keep your code tidy by running `ruff format` and `ruff check` or using vs code `ruff` extension
    - bobot won't give points if your file is not well formatted 

Extra materials:
- [about Model-View-Controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) and [even more about the same](https://www.techtarget.com/whatis/definition/model-view-controller-MVC)
- [we use blessed to render the simulation](https://blessed.readthedocs.io/en/latest/)
- [how the ruff linte  works](https://docs.astral.sh/ruff/linter//) and how can one use it via [a vs code extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) 

## Grading

* [ ] Make sure, you have a **private** group
  * [how to create a group](https://docs.gitlab.com/ee/user/group/#create-a-group)
* [ ] Fork this project into your private group
  * [how to create a fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork)
* [ ] Add @bobot-is-a-bot as the new project's member (role: **maintainer**)
  * [how to add an user](https://docs.gitlab.com/ee/user/project/members/index.html#add-a-user)

## How To Submit Solutions

* [ ] Clone repository: git clone:
    ```bash
    git clone <repository url>
    ```
* [ ] Solve the exercises
    * use WebIDE, whatever
* [ ] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [ ] Push changes to the gitlab master branch
    ```bash
    git push 
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file appears.

## Preparations

This assignment has been tested with >= Python 3.11.*. 
The simplest way to run the project is to create a virtual environment first:
 
- `python -m venv yatumas-venv`
- `source yatumas-venv/bin/activate`

Then install the requirements:

- `pip install -r requirements.txt`


## Project Structure

    .
    ├── examples                        # here we will store our machines 
    │   ├── add_one.tm
    │   ├── busy_beaver_3.tm
    │   └── busy_beaver_4.tm
    ├── yatumas
    │   ├── machine
    │   │   ├── action.py               # defines possible actions
    │   │   ├── machine.py              # class defining the machine
    │   │   ├── state.py                # defines a machine state type
    │   │   ├── symbol.py               # defines a symbol type
    │   │   └── transition_table.py     # contains types to define the transitions
    │   ├── parser
    │   │   ├── error.py                # defines the parsing errors
    │   │   └── parser.py               # functions to parse
    │   ├── simulator
    │   │   ├── controller.py           # TODO: a controller component of MVC
    │   │   ├── model.py                # TODO: a model component of MVC
    │   │   ├── simulation.py           # the main class responsible for simulation using MVC
    │   │   ├── simulation_state.py     # the possible simulation states
    │   │   ├── tape.py                 # a simple implementation of the infinite tape
    │   │   └── view.py                 # TODO: a view component of MVC
    │   └── __init__.py
    ├── README.md                       # file, you're reading right now 
    ├── requirements.txt                # TODO: install the requirements!
    ├── result.mp4                      # the expected result
    ├── ruff.toml                       # ruff settings for python 3.11
    └── yatumas.py                      # the `main` entrypoint.