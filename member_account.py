class State:
    """Represents the state of a member account. Contains all valid states."""

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
    """MemberAccount represents an account of a club member.

    After the member registers, the account must be confirmed to be active. When active, account information can be
    changed by the member. A member can suspend her account and reactivate it. If the annual fee is due, the account
    will be set inactive until the fee is paid by the member. A member can cancel the account to delete it.

    All methods change the state of the account, but only valid transition are possible. If an invalid transition
    is requested, methods will raise a RuntimeError. See _PossibleTransitions for all valid transitions.
    """
    _possible_transitions = _PossibleTransitions()

    def __init__(self):
        """Initializes the account to State START."""
        self.state = State.START

    def _transition(self, destination: State):
        if not self._possible_transitions.has_transition(self.state, destination):
            reachable_states = ", ".join([repr(s) for s in self._possible_transitions.get_reachable_states_from(self.state)])
            raise RuntimeError(f"Transition from '{self.state}' to '{destination}' invalid."
                               f" Reachable states are: {reachable_states}.")

        self.state = destination

    def register(self):
        """Sets the state of the account to REGISTERED after a new member registered."""
        self._transition(State.REGISTERED)

    def confirm(self):
        """Sets the state of the account to ACTIVE after the new member confirmed her mail address."""
        self._transition(State.ACTIVE)

    def change(self):
        """Updates member information and sets the state of the account to ACTIVE."""
        self._transition(State.ACTIVE)

    def suspend(self):
        """Sets the state of the account to DORMANT after the member suspended the account."""
        self._transition(State.DORMANT)

    def reactivate(self):
        """Sets the state of the account back to ACTIVE after the member reactivated her account."""
        self._transition(State.ACTIVE)

    def fee_due(self):
        """Sets the state of the account to INACTIVE because the annual fee is due."""
        self._transition(State.INACTIVE)

    def transfer(self):
        """Sets the state of the account back to ACTIVE after the member paid the annual fee."""
        self._transition(State.ACTIVE)

    def cancel(self):
        """Cancels the member account and sets the state of the account back to END."""
        self._transition(State.END)
