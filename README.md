## **State Machine / Workflow Engine Solution**

### Problem Breakdown
This problem involves designing a state machine or workflow engine that helps manage the states of a process in a system. The key idea is to track the progress of a workflow and the tasks in it, ensuring that when certain state transitions happen in one part of the workflow (for example, a task or the overall workflow), it can trigger corresponding state transitions in other parts.

### Key Components
- Workflow: Represents the overall process (e.g., Onboarding).
- Tasks: These are individual steps within the workflow (e.g., Sign Up, Verify Email, Add Profile).
- States: Represent the status of a workflow or task (e.g., Pending, In Progress, Completed).
- Links/Relationships: Define how the state of one component (Workflow or Task) affects others. For instance, if "Sign Up" moves to "In Progress," "Verify Email" and "Add Profile" might also need to move to "In Progress" as a result.


### Design Approach
#### State Enum
Create an enum class that will represent the possible states of a task or workflow.
```
class StateChoices(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
```

#### Task Class: 
Create a task class where each task has its own name, state, and can be linked to other tasks or workflows. In this class, we are adding two methods:
- set_state : This will set a new state for the task and will also change the state of the dependent task/workflow.
- add_link: Where we can define linked tasks/workflow.

```
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
```

#### Workflow Class: 
The workflow contains a name, state, tasks, and can also be linked to other tasks/workflows.

```
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
```


#### Link Class: 
This class represents the relationship between components (e.g., Task -> Task or Workflow -> Task) and is responsible for changing the state of dependent tasks/workflows.

- apply: This method checks if the source's state exists in the state mapping. If a transition is defined, it updates the target's state accordingly.

```
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
```
