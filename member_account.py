from state_machine import State, Transition, Transitions, StateMachine


class MemberAccount:
    """MemberAccount represents an account of a club member.

    After the member registers, the account must be confirmed to be active. When active, account information can be
    changed by the member. A member can suspend her account and reactivate it. If the annual fee is due, the account
    will be set inactive until the fee is paid by the member. A member can cancel the account to delete it.

    All methods change the state of the account, but only valid transition are possible. If an invalid transition
    is requested, methods will raise a RuntimeError. See _PossibleTransitions for all valid transitions.
    """

    START = State.START
    REGISTERED = State("registered")
    ACTIVE = State("active")
    INACTIVE = State("inactive")
    DORMANT = State("dormant")
    END = State.END

    _transitions = Transitions(Transition(START, "register", REGISTERED),
                               Transition(REGISTERED, "confirm", ACTIVE),
                               Transition(ACTIVE, "change", ACTIVE),
                               Transition(ACTIVE, "suspend", DORMANT),
                               Transition(ACTIVE, "fee due", INACTIVE),
                               Transition(ACTIVE, "cancel", END),
                               Transition(DORMANT, "reactivate", ACTIVE),
                               Transition(INACTIVE, "transfer", ACTIVE))

    def __init__(self):
        """Initializes the account to State START."""
        self.machine = StateMachine(MemberAccount._transitions)

    def get_state(self):
        """Returns the current state of the account."""
        return self.machine.state

    def register(self):
        """Sets the state of the account to REGISTERED after a new member registered."""
        self.machine.transition(self.REGISTERED)

    def confirm(self):
        """Sets the state of the account to ACTIVE after the new member confirmed her mail address."""
        self.machine.transition(self.ACTIVE)

    def change(self):
        """Updates member information and sets the state of the account to ACTIVE."""
        self.machine.transition(self.ACTIVE)

    def suspend(self):
        """Sets the state of the account to DORMANT after the member suspended the account."""
        self.machine.transition(self.DORMANT)
    
    def reactivate(self):
        """Sets the state of the account back to ACTIVE after the member reactivated her account."""
        self.machine.transition(self.ACTIVE)

    def fee_due(self):
        """Sets the state of the account to INACTIVE because the annual fee is due."""
        self.machine.transition(self.INACTIVE)

    def transfer(self):
        """Sets the state of the account back to ACTIVE after the member paid the annual fee."""
        self.machine.transition(self.ACTIVE)

    def cancel(self):
        """Cancels the member account and sets the state of the account back to END."""
        self.machine.transition(self.END)
