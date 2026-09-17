# research-lab-oop
Object-oriented research lab simulation — university coursework
# Research Lab Management System (OOP Coursework)

**Course:** Introduction to Programming, Ben-Gurion University of the Negev
**Assignment:** HW4 — Object-Oriented Programming
**Language:** Python 3 (standard library only — no external packages)

## Overview

A small object-oriented simulation of a university research lab. The system models researchers who run experiments, publish papers, and accumulate experience, all coordinated by a central `Lab` class that handles scheduling and assignment logic.

## Classes

- **`Researcher`** — represents a lab researcher with a field of specialization, experience level, current assignment, and list of published papers.
- **`Experiment`** — represents a timed research task tied to a specific field, which is assigned to a researcher and consumes time until completion.
- **`Paper`** — represents a publication that requires a set of experiments to be completed before it can be published, and tracks its authors and citations.
- **`Lab`** — the central coordinator: manages the pool of researchers and experiments, assigns experiments based on researcher availability and field-matched experience, advances simulation time, and tracks published papers.

## Key logic implemented

- Input validation with informative `TypeError` exceptions on all constructors.
- Custom `__repr__` methods for readable object output.
- Assignment logic in `Lab.assign_experiment`: prioritizes an available researcher whose field matches the experiment, falling back to the least-experienced available researcher when no field match exists.
- Time-based simulation via `advance_time`, which completes experiments and updates researcher availability/experience automatically.
- Paper publication logic that verifies all required experiments are complete before publishing and updates each contributing researcher's paper list.

## Notes

This was completed as a paired assignment for an introductory programming course. It reflects my level in Python at the time (control flow, functions, classes/OOP) rather than a professional software project.
