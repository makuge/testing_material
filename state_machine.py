class State:
    """Represents the state of an object. A state is essentially just a name."""

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.name == other.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


State.END = State("end")
State.START = State("start")


class Transition:
    def __init__(self, source: State, name: str, destination: State):
        self.source = source
        self.name = name
        self.destination = destination

    def __eq__(self, other):
        if not isinstance(other, Transition):
            return False
        return self.source == other.source and self.destination == other.destination

    def __repr__(self):
        return f"{self.source.name} -> {self.name} -> {self.destination.name}"


class Transitions(list):
    def __init__(self, *transitions):
        self.extend(transitions)

    def has_transition(self, source: State, destination: State):
        return Transition(source, None, destination) in self

    def get_reachable_states_from(self, source: State):
        return [t.destination for t in self if t.source == source]


class StateMachine:
    def __init__(self, transitions: Transitions):
        self.transitions = transitions
        self.state = State.START

    def in_states(self, *states):
        return self.state in states

    def transition(self, destination: State):
        if not self.transitions.has_transition(self.state, destination):
            reachable_states = ", ".join(
                [repr(s) for s in self.transitions.get_reachable_states_from(self.state)])
            raise RuntimeError(f"Transition from '{self.state}' to '{destination}' invalid."
                               f" Reachable states are: {reachable_states}.")

        self.state = destination
