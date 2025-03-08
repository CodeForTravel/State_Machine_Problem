from enum import Enum


# Define possible states
class StateChoices(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


# Task class representing a unit of work
class Task:
    def __init__(self, name):
        self.name = name
        self.state = StateChoices.PENDING
        self.links = []  # Links to other tasks or workflows

    def set_state(self, new_state):
        print(f"Task '{self.name}' changing state: {self.state.value} -> {new_state.value}")
        self.state = new_state
        for link in self.links:
            link.apply()

    def add_link(self, link):
        self.links.append(link)


# Workflow class managing multiple tasks
class Workflow:
    def __init__(self, name):
        self.name = name
        self.state = StateChoices.PENDING
        self.tasks = []
        self.links = []

    def add_task(self, task):
        self.tasks.append(task)

    def set_state(self, new_state):
        print(f"Workflow '{self.name}' changing state: {self.state.value} -> {new_state.value}")
        self.state = new_state
        for link in self.links:
            link.apply()

    def add_link(self, link):
        self.links.append(link)


# Link class defining state transition rules
class Link:
    def __init__(self, source, target, state_mapping):
        self.source = source
        self.target = target
        self.state_mapping = state_mapping  # Dict mapping source state -> target state

    def apply(self):
        if self.source.state in self.state_mapping:
            new_target_state = self.state_mapping[self.source.state]
            if self.target.state != new_target_state:
                self.target.set_state(new_target_state)


# Example: Setting up a simple onboarding workflow
if __name__ == "__main__":
    onboarding = Workflow("Onboarding")
    sign_up = Task("Sign Up")
    verify_email = Task("Verify Email")
    add_profile = Task("Add Profile")

    # Define relationships using links
    link1 = Link(sign_up, verify_email, {StateChoices.COMPLETED: StateChoices.IN_PROGRESS})
    link2 = Link(sign_up, add_profile, {StateChoices.COMPLETED: StateChoices.IN_PROGRESS})
    link3 = Link(verify_email, onboarding, {StateChoices.COMPLETED: StateChoices.COMPLETED})
    link4 = Link(add_profile, onboarding, {StateChoices.COMPLETED: StateChoices.COMPLETED})

    # Attach links
    sign_up.add_link(link1)
    sign_up.add_link(link2)
    verify_email.add_link(link3)
    add_profile.add_link(link4)

    # Add tasks to workflow
    onboarding.add_task(sign_up)
    onboarding.add_task(verify_email)
    onboarding.add_task(add_profile)

    # Simulate workflow progression
    sign_up.set_state(StateChoices.COMPLETED)
    verify_email.set_state(StateChoices.COMPLETED)
    add_profile.set_state(StateChoices.COMPLETED)
