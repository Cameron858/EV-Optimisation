# EV-Optimisation

This is a cool (imo) side project that I've been working on. I've always been interested in genetic algorithms so it was really fun to dig into the details of `NSGA-II` specifically. I first got the idea for the EV case study from this video [here](https://www.youtube.com/watch?v=SL-u_7hIqjA&ab_channel=paretos) and I thought it'd be fun to give it a go myself.

Key Learnings:
- Understanding the fundamentals of multi-objective optimisation, Pareto fronts and the NSGA-II algorithm.
- Implementing algorithms using a scientific paper as a primary guiding resource
- Gaining experience in implementing genetic algorithms in Python.
- Learning how to visualise trade-offs between conflicting objectives.
- Exploring the dynamics of EV performance metrics like range and acceleration.
- Enhancing skills in using tools like Poetry for dependency management.
- Deepening knowledge of Python-based simulation and optimisation techniques.

## Description
A Python-based tool for optimising electric vehicles (EV's) range and acceleration based on motor power and battery capacity.
This project is an implementation of `NSGA-II` [1].

## Table of Contents
- [Features](#features)
- [Installation](#installation)

## Features
- Simulate and evaluate acceleration dynamics.
- Generate a range of potential EV configurations based on motor power and battery capacity.
- Optimise configurations for maximum range and performance using NSGA-II.
- Provide visualisations for trade-offs between range and acceleration.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/EV-Optimisation.git
    ```

2. Navigate to the project directory:
    ```bash
    cd EV-Optimisation
    ```

3. Install Poetry if not already installed:
    ```bash
    pip install poetry
    ```

4. Install the required dependencies using Poetry:
    ```bash
    poetry install
    ```

5. Activate the virtual environment created by Poetry:
    ```bash
    poetry shell
    ```

### References

[1] K. Deb, A. Pratap, S. Agarwal, and T. Meyarivan. A fast and elitist multiobjective genetic algorithm: nsga-II. Trans. Evol. Comp, 6(2):182–197, April 2002. URL: http://dx.doi.org/10.1109/4235.996017, doi:10.1109/4235.996017.
