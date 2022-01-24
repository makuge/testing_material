class State:
    START, REGISTERED, ACTIVE, INACTIVE, DORMANT, END = "start", "registered", "active", "inactive", "dormant", "end"

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.name == other.name

    def __str__(self):
        return self.name


class _Transition:
    def __init__(self, source: State, name: str, destination: State):
        self.source = source
        self.name = name
        self.destination = destination

    def __eq__(self, other):
        if not isinstance(other, _Transition):
            return False
        return self.source == other.source and self.destination == other.destination

    def __repr__(self):
        return f"{self.source.name} -> {self.name} -> {self.destination.name}"


class _PossibleTransitions(list):
    def __init__(self):
        self.append(_Transition(State.START, "register", State.REGISTERED))

        self.append(_Transition(State.REGISTERED, "confirm", State.ACTIVE))

        self.append(_Transition(State.ACTIVE, "change", State.ACTIVE))
        self.append(_Transition(State.ACTIVE, "suspend", State.DORMANT))
        self.append(_Transition(State.ACTIVE, "fee due", State.INACTIVE))
        self.append(_Transition(State.ACTIVE, "cancel", State.END))

        self.append(_Transition(State.DORMANT, "reactivate", State.ACTIVE))

        self.append(_Transition(State.INACTIVE, "transfer", State.ACTIVE))

    def has_transition(self, source: State, destination: State):
        return _Transition(source, None, destination) in self

    def get_reachable_states_from(self, source: State):
        return [t.destination for t in self if t.source == source]


class MemberAccount:
    _possible_transitions = _PossibleTransitions()

    def __init__(self):
        self.state = State.START

    def _transition(self, destination: State):
        if not self._possible_transitions.has_transition(self.state, destination):
            reachable_states = ", ".join([repr(s) for s in self._possible_transitions.get_reachable_states_from(self.state)])
            raise RuntimeError(f"Transition from '{self.state}' to '{destination}' invalid."
                               f" Reachable states are: {reachable_states}.")

        self.state = destination

    def register(self):
        self._transition(State.REGISTERED)

    def confirm(self):
        self._transition(State.ACTIVE)

    def change(self):
        self._transition(State.ACTIVE)

    def suspend(self):
        self._transition(State.DORMANT)

    def reactivate(self):
        self._transition(State.ACTIVE)

    def fee_due(self):
        self._transition(State.INACTIVE)

    def transfer(self):
        self._transition(State.INACTIVE)

    def cancel(self):
        self._transition(State.END)
