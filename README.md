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
        if self.remaining_hours <= 0:
            self.remaining_hours = 0
            self.completed = True
            self.researcher.finish_experiment()
        return None


class Paper:
    def __init__(self, name, required_experiments):
        # name must be a non-empty string
        if not isinstance(name, str) or name == '':
            raise TypeError('Invalid name for Paper')
        # required_experiments must be a list (an empty list is allowed)
        if not isinstance(required_experiments, list):
            raise TypeError('Invalid required_experiments for Paper')
        self.name = name
        self.required_experiments = required_experiments
        self.authors = []
        self.citations = 0
        self.is_published = False

    def __repr__(self):
        # builds the string representation of the paper, showing the authors by name only
        author_names = [researcher.name for researcher in self.authors]
        return f"Paper: {self.name}, authors: {author_names}, is published? {self.is_published}"

    def add_citation(self):
        # adds a citation to the paper
        self.citations += 1
        return None

    def publish(self):
        # if the paper is already published, notify and return True
        if self.is_published:
            print("The paper already been published")
            return True

        # count how many required experiments are not completed yet
        unfinished_count = 0
        for experiment in self.required_experiments:
            if not experiment.completed:
                unfinished_count += 1

        if unfinished_count > 0:
            print(f"There are more {unfinished_count} experiments to finish")
            return False

        # all required experiments are completed - gather the authors
        authors = []
        author_names = []
        for experiment in self.required_experiments:
            researcher = experiment.researcher
            if researcher is not None and researcher not in authors:
                authors.append(researcher)
                author_names.append(researcher.name)
                researcher.papers.append(self.name)

        self.authors = authors
        self.is_published = True
        print(author_names)
        return True


class Lab:
    def __init__(self, name):
        # name must be a non-empty string
        if not isinstance(name, str) or name == '':
            raise TypeError('Invalid name for Lab')
        self.name = name
        self.researchers = []
        self.experiments = []
        self.papers = {}

    def __repr__(self):
        # builds the string representation of the lab, as required by the assignment file
        return f"Lab: {self.name}, Researchers: {len(self.researchers)}, Amount of papers: {len(self.papers)}"

    def add_researcher(self, researcher):
        # adds a new researcher to the lab, unless they are already part of it
        if researcher in self.researchers:
            return False
        self.researchers.append(researcher)
        return True

    def add_experiment(self, experiment):
        # adds a new experiment to the lab, unless it is already part of it
        if experiment in self.experiments:
            return False
        self.experiments.append(experiment)
        return True

    def advance_time(self, hours):
        # advance the time for every experiment linked to this lab
        for experiment in self.experiments:
            experiment.advance_time(hours)
        return None

    def assign_experiment(self, experiment):
        # if the experiment already has a researcher assigned, notify and stop
        if experiment.researcher is not None:
            print(f"The experiment {experiment.name} already been assigned to Researcher {experiment.researcher.name}")
            return None

        # if there are no researchers in the lab at all, notify and stop
        if len(self.researchers) == 0:
            print("There are no researchers")
            return None

        available_researchers = [researcher for researcher in self.researchers if researcher.is_available()]
        if len(available_researchers) == 0:
            # no available researcher right now - nothing to do
            return None

        # first, look for a researcher whose field matches the experiment's field
        same_field_researchers = [researcher for researcher in available_researchers if researcher.field == experiment.field]

        if len(same_field_researchers) > 0:
            # choose the researcher with the most experience in that field
            # (ties are broken by whoever appears first, i.e. joined the lab earlier)
            chosen = same_field_researchers[0]
            for researcher in same_field_researchers[1:]:
                if researcher.experience > chosen.experience:
                    chosen = researcher
        else:
            # no researcher matches the field - choose the one with the least experience
            chosen = available_researchers[0]
            for researcher in available_researchers[1:]:
                if researcher.experience < chosen.experience:
                    chosen = researcher

        experiment.assign_researcher(chosen)

        if experiment not in self.experiments:
            self.experiments.append(experiment)

        return None

    def assign_multiple_experiments(self, experiment_list):
        # assign a researcher to each experiment in the given list
        # (assign_experiment already takes care of adding the experiment to the lab)
        for experiment in experiment_list:
            self.assign_experiment(experiment)
        return None

    def updated_and_get_papers(self):
        # rebuild the papers dictionary from the researchers' personal paper lists:
        # key = paper name, value = list of names of researchers who wrote it
        self.papers = {}
        for researcher in self.researchers:
            for paper_name in researcher.papers:
                if paper_name not in self.papers:
                    self.papers[paper_name] = []
                if researcher.name not in self.papers[paper_name]:
                    self.papers[paper_name].append(researcher.name)
        return self.papers
