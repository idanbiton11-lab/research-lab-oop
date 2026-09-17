class Researcher:
    def __init__(self, name, field=''):
        # name must be a non-empty string
        if not isinstance(name, str) or name == '':
            raise TypeError('Invalid name for Researcher')
        # field can be an empty string, but must be a string
        if not isinstance(field, str):
            raise TypeError('Invalid field for Researcher')
        self.name = name
        self.field = field
        self.experience = 0
        self.current_experiment = None
        self.papers = []
        self.available = True

    def __repr__(self):
        # builds the string representation of the researcher, as required by the assignment file
        return f"Researcher: {self.name}, Field: {self.field}, .Papers: {self.papers}"

    def is_available(self):
        # returns whether the researcher can be assigned a new experiment
        return self.available

    def get_status(self):
        # returns a tuple: (current experiment, experience points)
        return (self.current_experiment, self.experience)

    def finish_experiment(self):
        # called when the researcher's current experiment is completed
        self.experience += 1
        self.current_experiment = None
        self.available = True
        return None


class Experiment:
    def __init__(self, name, field, remaining_hours):
        # name must be a non-empty string
        if not isinstance(name, str) or name == '':
            raise TypeError('Invalid name for Experiment')
        # field is a string that describes the experiment's domain (an empty string is allowed)
        if not isinstance(field, str):
            raise TypeError('Invalid field for Experiment')
        # remaining_hours must be an int greater than 0
        if not isinstance(remaining_hours, int) or isinstance(remaining_hours, bool) or remaining_hours <= 0:
            raise TypeError('Invalid remaining_hours for Experiment')
        self.name = name
        self.field = field
        self.remaining_hours = remaining_hours
        self.completed = False
        self.researcher = None

    def __repr__(self):
        # builds the string representation of the experiment, as required by the assignment file
        return f"Experiment: {self.name}, Field: {self.field}, Remaining hours: {self.remaining_hours}"

    def assign_researcher(self, researcher):
        # an experiment can only be assigned once, and only to an available researcher
        if self.researcher is not None or self.completed:
            return False
        if not researcher.is_available():
            return False
        self.researcher = researcher
        researcher.current_experiment = self
        researcher.available = False
        return True

    def advance_time(self, hours):
        # if the experiment is already completed or has no researcher, do nothing
        if self.completed or self.researcher is None:
            return None
        self.remaining_hours -= hours
        if self.remaining_hours 
