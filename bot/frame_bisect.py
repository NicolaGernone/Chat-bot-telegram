from config import logger as lg


class FrameBisection:
    def __init__(self):
        self.reset()

    def reset(self):
        """
        Resets the frame bisection state.
        """
        self.lower_bound = 0
        self.upper_bound = 61696
        self._current_frame = (self.lower_bound + self.upper_bound) // 2
        lg.info("Frame bisection state has been reset.")

    @property
    def current_frame(self) -> int:
        """
        Property that returns the current frame.
        """
        return self._current_frame
    
    @current_frame.setter
    def current_frame(self, value: int) -> None:
        """
        Setter for the current frame.
        """
        self._current_frame = value

    def update_bounds(self, response: str) -> None:
        """
        Updates the bisection bounds based on the user's response.
        """
        lg.info(f"Updating bounds based on response: {response}")
        if response == "yes":
            self.upper_bound = self._current_frame
        else:
            self.lower_bound = self._current_frame

        # Update the current frame after adjusting bounds
        self._current_frame = (self.lower_bound + self.upper_bound) // 2
        lg.info(f"Next frame to check: {self._current_frame}")
