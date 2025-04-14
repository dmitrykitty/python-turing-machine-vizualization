from timeit import default_timer as timer
import blessed
from yatumas.machine.transition_table import Transition
from yatumas.simulator.simulation_state import SimulationState # noqa
from yatumas.simulator.view import View
from yatumas.simulator.model import Model


class Controller:
    """
    Class responsible for controlling the simulation.

    Protected Attributes
    ----------
    _model: Model
        contains all the data required by the simulation
    _view View
        display the simulation to the user
    _term: blessed.Terminal
        used to gather input from the terminal

    Methods
    -------
    def run_simulation() -> None:
        runs the simulation
    """

    _model: Model
    _view: View
    _term: blessed.Terminal

    def __init__(self, model: Model, view: View, term: blessed.Terminal):
        """
        Initializes the controller.

        Parameters
        ----------
        model: Model
            corresponds to the self._model attribute
        view: View
            corresponds to the self._view attribute
        erm: blessed.Terminal
            correspond to the self._term attribute
        """
        self._model = model
        self._view = view
        self._term = term

    def run_simulation(self):
        """
        Runs the simulation
        """
        # TODO:
        # Implement the main simulation loop.
        # 1. Use self._view as a context manager (`with ...`)
        # 2. Refresh the screen once and run the input loop
        # 3. Make a loop, while the self._step() returns True
        #   - refresh the screen
        #   - run the input loop
        # 4. after the loop refresh the screen
        #    and wait for any user input
        #
        # tips: read docstrings of the Controller and View classes
        raise NotImplementedError()

    def _find_applicable_transition(self) -> Transition | None:
        """
        Helper method to find the currently applicable transition.

        Returns
        -------
        transition: Transition | None
            an applicable transition, if there is any, otherwise None
        """
        condition = self._model.current_condition
        if effect := self._model.machine.transition_table.get(condition, None):
            return Transition(condition, effect)
        return None

    def _step(self) -> bool:
        """
        Makes a single step of the simulation.

        Returns
        -------
        should_continue: bool
            True - if the simulation should continue
            False - if the simulation has finished
        """

        # TODO:
        # Make a single step of the simulation 
        # based on the `simulator_state` stored in the `model`
        #
        # hint: it is easies to use the match statement: 
        #   https://docs.python.org/3/tutorial/controlflow.html#match-statements
        # 
        # 1. if the simulation is `idle``, find a next TM transition
        #   - if there is no transition, state changes to `finished`
        #   - if there is a transition, store it in the model
        #     and change state to `found transition`
        #   - return `True`  
        # tip. use the `_find_applicable_transition` helper
        # 
        # 2. if the simualation just found a transition:
        #   - update the `machine_state` and write a new symbol to the tape
        #     according to the transition
        #   - change state to `changed_state`
        #   - return `True`
        #
        # 3. if the simulation has just changed the state:
        #   - update the head position in the model according to the transition
        #   - change simulation state to `moved`
        #   - return `True``
        # 
        # 4. if the simulation has just moved the head:
        #   - update the state to `idle` and clear the transition in the model
        #   - return `True`
        #
        # 5. if the simulation has ended (states `finished` and `interrupted`)
        #   - just return `False`
        #
        raise NotImplementedError()

    def _wait_for_any_key(self) -> None:
        """
        Waits indefinitely for any key to be pressed.
        """
        with self._term.cbreak():           # to read the user input from the terminal
            self._term.inkey(timeout=None)  # wait for an input indefinetely

    def _run_input_loop(self) -> None:
        """
        Reacts to the user input:
        - 's' -> slows down the simulation
        - 'a' -> accelerates the simulation
        - 'q' -> quits the simulation
        """
        
        start = timer() # noqa <- for ruff check to ignore

        def time_left() -> float: # noqa <- for ruff check to ignore
            # TODO:
            # Return how much time we have left in the current simulation step.
            # hints:
            #     - `self._model.step_interval_in_sec` is the total available time
            #    - `start` is when we have started
            #    - `timer` is a function from the timeit module telling the current time   
            return NotImplemented

        # TODO:
        # Implement an event loop waiting for the user input.
        # 1. open the cbreak context like in the `_wait_for_any_key`
        # 2. create a loop going as long as there is any time left
        #   hint. implement and use the local function `time_left`
        # 3. inside the loop:
        #   - wait for the user input as long as we have time left
        # 4. depending on the input:
        #   - `s` > increase the `step_interval_in_sec` by 0.1
        #   - `a` > decrease the `step_interval_in_sec` by 0.1
        #           also make sure it never goes below 0.1
        #   - `q` > change the simulator state to `INTERRUPTED`
        raise NotImplementedError()
