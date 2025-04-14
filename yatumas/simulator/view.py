from collections.abc import Callable #noqa
from typing import Literal #noqa
import blessed
from yatumas.machine.symbol import Symbol #noqa
from yatumas.simulator.simulation_state import SimulationState
from yatumas.simulator.model import Model


class View:
    """
    Class responsible for displaying the simulation.
    Expected to be used as a context manager:

        with view() as refresh:
            refresh() # < refreshes the screen

    Protected Attributes
    ----------
    _ellipsis: str
        symbol to be printed at the ends of the tape
    _separator: str
        symbol used to separate symbols on the tape
    _term: blessed.Terminal
        a terminal object used to print correct output codes
    _model: Model
        a model component of the simulation
    _head_x_coordinate: int | None
        current position of the TM's head, if any

    Methods
    -------
    def __init__(model: Model, term: blessed.Terminal):
        initialiaes the view component
    def __enter__() -> Callable[[], None]:
        entering the context manager prepares the terminal
        and returns a handle to refresh the screen
    def __exit__(*args) -> None:
        when exiting, the terminal returns to its normal mode
    """

    _ellipsis = "..."
    _separator = "|"
    _term: blessed.Terminal
    _model: Model
    _head_x_coordinate: int | None

    def __init__(self, model: Model, term: blessed.Terminal):
        """
        Initializes the object.

        Parameters
        ----------
        model: Model
            corresponds to the self._model attribute
        term: blessed.Terminal
            correspond to the self._term attribute
        """
        self._model = model
        self._term = term
        self._reset()

    def _reset(self):
        """
        Reset the view state.
        """
        self._head_x_coordinate = None


    # TODO:
    # Implement the context manager magical methods
    # __enter__ and __exit__
    # - https://docs.python.org/3/library/stdtypes.html#context-manager-types
    # The docstrings are already there.
    #
    # 1. entering context should:
    #   - reset the view state
    #   - prepare the terminal via self._term.enter_fullscreen()
    #   - return the self._refresh function
    # 2. exitting context should:
    #   - should exit the fullscreen
    #   - should not suppress exceptions
    """
        Enters the view context: clearing the view and entering the fullscreen.

        Returns
        -------
        refresh: Callable[[], None]
            the "refresh" callback
    """

    """
        Cleans the context, exitting the fullscreen.
    """

    def _refresh(self) -> None:
        """
        Refreshes the simulation view.
        """
        print(self._clear_screen())
        print(self._term.center(self._display_title()))
        print()
        print(self._display_tape())
        print()
        print(self._term.center(self._display_transition()))
        print()
        print(self._term.center(self._display_footer()))

    def _clear_screen(self) -> str:
        """
        Return a terminal sequence clearing the terminal screen
        """
        return self._term.home + self._term.on_black + self._term.clear

    def _display_title(self) -> str:
        """
        Returns a formatted app header
        """
        return self._title_font("Yet Another Turing Machine Simulator")

    def _display_tape(self) -> str:
        """
        Returns a string representing a well-formatted tape.
        """

        head_x_coordinate = self._updated_head_x_coordinate()
        symbols = self._visible_symbols(head_x_coordinate)

        # what is the symbol below the head ?
        head_symbol_index = next(
            i for i, (si, _) in enumerate(symbols) if si == self._model.head_offset
        ) 

        # splits symbols into three parts:
        # before, below, after the head 
        symbols_before_head = [s for _, s in symbols[:head_symbol_index]]
        head_symbol = symbols[head_symbol_index][1]
        symbols_after_head = [s for _, s in symbols[head_symbol_index + 1 :]]

        # renders the symbols according to the positions
        # - the head symbol is selected
        # underline makes the floor of the tape
        before_head = self._separator.join([self._ellipsis] + symbols_before_head)
        head = self._separator + head_symbol + self._separator
        after_head = self._separator.join(symbols_after_head + [self._ellipsis])
        tape_line = (
            self._normal_underlined_font(before_head)
            + self._selected_underlined_font(head)
            + self._normal_underlined_font(after_head)
        )

        # renders the state string, centering it aorund the head position
        state = self._model.machine_state
        left_state_half = state[: max(0, len(state) // 2 - 1)]
        state_center = state[len(left_state_half) : len(left_state_half) + 3]
        right_state_half = state[len(left_state_half) + len(state_center) :]

        # render the "ceiling" of the tape,
        # there are five types of the cealing:
        # - before the machine state
        # - before the head position
        # - the head position
        # - after the head, before the end of the state string
        # - after machine state
        above_before_state = " " * (
            len(before_head) - len(left_state_half) - len(state_center) // 2
        )
        above_before_head = self._separator + left_state_half if left_state_half else ""
        above_head = (
            ("" if left_state_half else self._separator)
            + state_center
            + ("" if right_state_half else self._separator)
        )
        above_after_head = (
            right_state_half + self._separator if right_state_half else ""
        )
        above_after_state = " " * (
            len(after_head) - len(right_state_half) - len(state_center) // 2
        )
        above_line = (
            self._normal_underlined_font(above_before_state)
            + self._selected_underlined_font(above_before_head)
            + self._selected_font(above_head)
            + self._selected_underlined_font(above_after_head)
            + self._normal_underlined_font(above_after_state)
        )

        # we return the ceiling + the tape itself
        return above_line + "\n" + tape_line

    def _n_symbols(self) -> int:
        # TODO:
        # Count how many symbol will fit on the screen.
        # 
        # tips:
        #   - look at the docstring
        #   - `self._term_width` is the width of the terminal
        """
        Tells how many symbol can fit on the screen

        Returns
        --------
        n_symbol: int
            number of the symbol that will fit in the terminal, assuming
            - there are two self._ellipsis at the ends separated by a single space character
            - the self.separator is used to separate the symbols
        """
        raise NotImplementedError()
    
    def _movement_direction(self) -> int:
        # TODO:
        # Return the position change of the head.
        # - position changes only if the simulation state is `MOVED`
        # - otherwise there are two possibilites:
        #   a) head is currently somewhere in the center of the terminal
        #       | left margin |             center              | right margin |
        #       |     10%     |               80%               |     10%      |
        #   b) head is on the brink of the screen (within left/right margin)
        #  
        #   In case a) we can just return the last move stored in the model.
        #   In case b) we make sure the head doesn't move past screen:
        #       e.g. if head is in the left margin and moves left, return 0
        """
        Tells how the head x coordinate should change on the screen.

        Returns
        -------
        offset: int
            if positive (typically +1), head moves right by the value
            if negative (typically -1), head moves left by the value
        """
        raise NotImplementedError()

    def _updated_head_x_coordinate(self) -> int:
        """
        Updates the head `x` coordinate (`self._head_x_coordinate`)
        and return the new value.

        Returns
        -------
        x_coordinate: int
            the new coordinate of the head
        """
        move = self._movement_direction()
        n_symbols = self._n_symbols()
        self._head_x_coordinate = (
            n_symbols // 2
            if self._head_x_coordinate is None
            else self._head_x_coordinate + move
        )
        return self._head_x_coordinate

    def _visible_symbols(self, head_x_coordinate: int) -> list[(tuple[int, str])]:
        # TODO:
        # To render the tape, we need to render all and only the visible symbols.
        # 1. we need to identify the visible part of the tape
        #   * hints:
        #     - use `_n_symbols` method to find how many symbols are to be displayed
        #     - knowing the `head_x_coordinate` and `head_offset` in the _model:
        #       > assume the `head_x_coordinate` is the number of visible symbols with 
        #         `index <= head_offset`
        #       > in the same way, we can count how many symbols are visible on the right side of the head
        #       > using `head_offset` as the reference point, you can calculate the visible range
        # 2. we need to return visible symbols as a list of tuples (as in the docstring)
        
        """
        Returns a list of rendered symbols to be displayed.

        Parameters
        ----------
        head_x_coordinate: int
            the current head position on the screen
        
        Returns
        -------
        symbol: list[tuple[int, str]]
            a list of tuples containing:
            - index of the symbol on the tape
            - rendered symbol ('_' replaced with ' ')
        """
        raise NotImplementedError()

    def _display_transition(self) -> str:
        # TODO:
        # We need to return a formatted string representing the current transition
        # 1. if we are in the `IDLE` state, return "...looking for transition"
        #    formatted with the normal font 
        #    - for reference, `_display_tape` uses various fonts a lot
        # 2. if simulation has finished, return "FINISHED"
        #    formated with the title font
        # 3. if simulation has been interrupted, return "INTERRUPTED"
        #    formatted with the title font
        # 4. Otherwise return string represting the current transition:
        #       condition.state + condition.symbol |> effect.new_state + effect.new_symbol |> effect.action
        #    formatted with normal font, except:
        #       - if state equals FOUND_TRANSITION, the condition.state + condition.symbol should use the selected font
        #       - if state equals CHANGED_STATE, the effect.new_state + effect.new_symbol should use the selected fontt
        #       - if state equals MOVE, the effect.action should use the selected font
        """
        Returns a sequence representing the currently chosen transition.
        """
        raise NotImplementedError()

    def _display_footer(self) -> str:
        """
        Returns a sequence representing the application footer.
        """
        match self._model.simulator_state:
            case SimulationState.FINISHED | SimulationState.INTERRUPTED:
                return "Press Any Key to Exit"
            case _:
                return f" [a] - accelerate | [s] - slow down | [q] - quit | current refresh interval: {self._model.step_interval_in_sec:.1f} s"

    def _normal_underlined_font(self, text: str = ""):
        """
        Returns a text formatted as the "normal" underlined font.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._normal_font(self._term.underline + text) + self._normal_font()

    def _normal_font(self, text: str = ""):
        """
        Returns a text formatted using the "normal" font.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._term.normal + self._term.white_on_black + text

    def _selected_underlined_font(self, text: str = ""):
        """
        Returns a text formatted using the "selected" font with the underline effect.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._term.underline + self._selected_font(text)

    def _selected_font(self, text: str = ""):
        """
        Returns a text formatted using the "selected" font.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._term.bold + self._term.black_on_white + text + self._normal_font()

    def _title_font(self, text: str = ""):
        """
        Returns a text formatted using the "title" font.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return (
            self._term.white_on_black
            + self._term.bold
            + self._term.underline
            + text
            + self._normal_font()
        )
