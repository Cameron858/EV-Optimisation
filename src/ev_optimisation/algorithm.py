import random
from ev_optimisation.operators import mutate, sbx_crossover
from ev_optimisation.pipelines import evaluate_population
from ev_optimisation.vehicle import Vehicle, VehicleConfig, GenerationResult
import numpy as np


def create_random_vehicle() -> Vehicle:
    """
    Create a single Vehicle instance with random motor power and battery capacity.

    Returns
    -------
    Vehicle
        A Vehicle instance with randomly generated attributes.
    """
    power = random.uniform(*Vehicle.MOTOR_POWER_BOUNDS)
    power = round(power, 2)

    capacity = random.uniform(*Vehicle.BATTERY_CAPACITY_BOUNDS)
    capacity = round(capacity, 2)

    return Vehicle(motor_power=power, battery_capacity=capacity)


def create_population(size: int) -> list[Vehicle]:
    """
    Create a population of Vehicle instances with random attributes.

    Parameters
    ----------
    size : int
        The number of Vehicle instances to create.

    Returns
    -------
    list[Vehicle]
        A list of Vehicle instances with randomly generated attributes.
    """
    return [create_random_vehicle() for _ in range(size)]


def pareto_dominance(i1: np.ndarray, i2: np.ndarray) -> bool:
    """
    Check if `i1` dominates `i2` in a Pareto sense.

    `i` -> `individual`

    Parameters
    ----------
    i1 : np.ndarray
        The objective values of the first individual.
    i2 : np.ndarray
        The objective values of the second individual.

    Returns
    -------
    bool
        True if `i1` dominates `i2`, False otherwise.
    """
    # i1 dominates i2 if it is at least as good in all objectives and strictly better in at least one
    # assumes all objectives are to minimise
    return np.all(i1 <= i2) and np.any(i1 < i2)


def assign_fronts(p_obj: np.ndarray) -> dict[int, set[int]]:
    """
    Assign Pareto fronts to a population based on objective values.

    Parameters
    ----------
    p_obj : np.ndarray
        A (N, M) array where N is the number of individuals and M is the number of objectives.

    Returns
    -------
    dict[int, set[int]]
        A dictionary mapping front number to sets of individual indices belonging to that front.
    """
    # initialise first front
    F = {1: set()}

    # S -> "dominates" counter
    S = {i: set() for i in range(p_obj.shape[0])}

    # n -> "domination" counter i.e. "dominated by"
    n = np.zeros(p_obj.shape[0])

    # find members of F1
    for p_idx, p in enumerate(p_obj):

        for q_idx, q in enumerate(p_obj):

            # do not compare same individuals
            if p_idx == q_idx:
                continue

            # if p dominates q, add q to the set of solutions dominated by p
            if pareto_dominance(p, q):
                S[p_idx].add(q_idx)
            # if q dominated p, increase the domination counter of p
            elif pareto_dominance(q, p):
                n[p_idx] += 1

        if n[p_idx] == 0:
            F[1].add(p_idx)

    # populate the rest of the fronts
    i = 1
    while len(F[i]) != 0:

        # init members of next front
        Q = set()

        for p in F[i]:
            for q in S[p]:
                n[q] -= 1

                if n[q] == 0:
                    Q.add(q)

        # avoid empty last set
        if not Q:
            break
        i += 1
        F[i] = Q

    # check no members have been left out
    assert p_obj.shape[0] == len(set().union(*F.values()))

    return F


def flatten_fronts(p_obj: np.ndarray, fronts: dict[set[int]]) -> np.ndarray:
    """
    Assign a front number to each individual in the population based on the provided fronts.

    Parameters
    ----------
    p_obj : np.ndarray
        A 2D array where each row represents an individual and each column represents an objective value.
    fronts : dict of set of int
        A dictionary where the keys are front numbers (starting from 0) and the values are sets of indices
        corresponding to individuals in that front.

    Returns
    -------
    np.ndarray
        A 1D array where each element corresponds to the front number assigned to the respective individual
        in the population.
    """
    f = np.zeros(p_obj.shape[0])
    for front, members in fronts.items():
        f[list(members)] = front
    return f


def calculate_crowding_distance(p_obj: np.ndarray) -> np.ndarray:
    """
    Calculate the crowding distance for each individual.

    Parameters
    ----------
    p_obj : np.ndarray
        A (N, M) array where N is the number of individuals and M is the number of objectives.

    Returns
    -------
    np.ndarray
        An array of crowding distances for each individual.
    """
    crowding_distances = np.zeros(p_obj.shape[0])

    # For each objective m
    for m in range(p_obj.shape[1]):
        m_values = p_obj[:, m]

        m_range = m_values.max() - m_values.min()

        # Sort m
        m_sorted_indices = np.argsort(m_values)

        # Set the crowding distance for the boundary points to inf
        # this is so later these points will always be chosen over other members in the same front,
        # therefore promoting diversity
        boundary_indices = m_sorted_indices[[0, -1]]
        crowding_distances[boundary_indices] = np.inf

        # Update the in-between points
        for i in range(1, m_sorted_indices.shape[0] - 1):
            prev_i = m_sorted_indices[i - 1]
            next_i = m_sorted_indices[i + 1]

            increment = (m_values[next_i] - m_values[prev_i]) / m_range
            crowding_distances[m_sorted_indices[i]] += increment

    return crowding_distances


def tournament_select(
    p_obj: np.ndarray, fronts: dict[set[int]], crowding_distances: np.ndarray
) -> int:
    """
    Perform tournament selection based on Pareto fronts and crowding distances.

    Parameters
    ----------
    p_obj : np.ndarray
        The population objective values, where each row corresponds to an individual
        and each column corresponds to an objective.
    fronts : dict[set[int]]
        A list of Pareto fronts, where each front is a list of indices corresponding
        to individuals in the population.
    crowding_distances : np.ndarray
        An array of crowding distances for each individual in the population.

    Returns
    -------
    int
        The index of the selected individual from the population.
    """
    fronts = flatten_fronts(p_obj, fronts)

    members = np.array(list(zip(fronts, crowding_distances)))
    selected_i = np.random.choice(p_obj.shape[0], 2, replace=False)
    selected = members[selected_i]

    # sort by front (ascending), then by crowding distance (descending, so we negate)
    winner_rel_i = np.lexsort((-selected[:, 1], selected[:, 0]))[0]
    winner_abs_i = selected_i[winner_rel_i]

    return winner_abs_i


def generate_offspring(
    p: np.ndarray,
    p_obj: np.ndarray,
    fronts: np.ndarray,
    crowding_distances: np.ndarray,
    crossover_rate: float = 0.9,
    mutate_rate: float = 0.05,
) -> list[Vehicle]:
    """
    Generate offspring using tournament selection, SBX crossover, and polynomial mutation.

    Parameters
    ----------
    p : np.ndarray
        Current population.
    p_obj : np.ndarray
        Objective values of the current population.
    fronts : np.ndarray
        Array indicating the front number for each individual.
    crowding_distances : np.ndarray
        Crowding distances for each individual.
    crossover_rate : float, optional
        Probability of performing SBX crossover, by default 0.9.
    mutate_rate : float, optional
        Probability of applying polynomial mutation to each child, by default 0.05.

    Returns
    -------
    list[Vehicle]
        New offspring population of the same size as the original.
    """
    mating_pool = []
    while len(mating_pool) < len(p):

        # select a winner
        winner_i = tournament_select(p_obj, fronts, crowding_distances)
        mating_pool.append(p[winner_i])

    assert len(mating_pool) == len(p)

    # breed in pairs
    Q = []
    for i in range(0, len(p), 2):

        p1 = mating_pool[i]
        p2 = mating_pool[i + 1]

        # roll for crossover, else propagate parents as children
        if np.random.rand() < crossover_rate:
            children = sbx_crossover(p1, p2)
        else:
            children = p1, p2

        # independantly mutate children
        children = [mutate(c, mutate_rate) for c in children]

        Q.extend(children)

    assert len(Q) == len(p)

    return Q


def propagate_species(
    p: list[Vehicle], q: list[Vehicle], config: VehicleConfig
) -> list[Vehicle]:
    """
    Combine two populations of vehicles, evaluates their fitness, and selects
    the top half based on non-dominated sorting and crowding distance.

    Parameters
    ----------
    p : list[Vehicle]
        The first population of vehicles.
    q : list[Vehicle]
        The second population of vehicles.
    config : VehicleConfig
        Configuration object containing parameters for vehicle evaluation.

    Returns
    -------
    list[Vehicle]
        The selected top half of the combined population after evaluation.
    """
    assert len(p) == len(q)

    r = [*p, *q]

    r_obj = evaluate_population(r, config)
    r_fronts = assign_fronts(r_obj)
    r_fronts = flatten_fronts(r_obj, r_fronts)
    r_crowding_dists = calculate_crowding_distance(r_obj)

    x = np.column_stack((r_fronts, r_crowding_dists))
    i = np.lexsort((-x[:, 1], x[:, 0]))
    top_n_indices = i[: i.shape[0] // 2]
    p = np.array(r)[top_n_indices]

    return p


def population_to_array(population: list[Vehicle]) -> np.ndarray:
    """
    Convert a population of vehicles into a numpy array.

    Parameters
    ----------
    population : list[Vehicle]
        A list of Vehicle objects. Each Vehicle object should have attributes:
        - motor_power: float
        - battery_capacity: float
        - mass(): callable that returns the mass of the vehicle as a float.

    Returns
    -------
    np.ndarray
        A 2D numpy array where each row represents a vehicle and contains:
        - motor_power (float)
        - battery_capacity (float)
        - mass (float)
    """
    return np.array([[v.motor_power, v.battery_capacity, v.mass()] for v in population])


def optimise_ev_population(
    config, n_gens, n_pop=None, initial_population=None
) -> dict[int, GenerationResult]:
    """
    Optimise an EV population using NSGA-II.

    Parameters
    ----------
    config : VehicleConfig
        Configuration for the vehicles.
    n_gens : int
        Number of generations to evolve.
    n_pop : int, optional
        Number of individuals in the population. If `initial_population` is provided, this is ignored.
    initial_population : list[Vehicle], optional
        An optional initial population of vehicles. If not provided, a new population will be created.

    Returns
    -------
    dict[int, GenerationResult]
        A dictionary where the keys are generation numbers and the values are GenerationResult objects
    """
    if initial_population is not None:
        n_pop = len(initial_population)
    elif n_pop is None:
        raise ValueError("Either `n_pop` or `initial_population` must be provided.")

    p = (
        initial_population
        if initial_population is not None
        else create_population(n_pop)
    )

    result = {}
    for generation in range(n_gens + 1):

        # Evaluate the population
        p_obj = evaluate_population(p, config)

        # Assign fronts and calculate crowding distances
        fronts = assign_fronts(p_obj)
        crowding_distances = calculate_crowding_distance(p_obj)

        result[generation] = GenerationResult(
            generation=generation,
            population=p,
            fronts=flatten_fronts(p_obj, fronts),
            objectives=p_obj,
            distances=crowding_distances,
        )

        # Generate offspring and propagate species
        q = generate_offspring(p, p_obj, fronts, crowding_distances)
        p = propagate_species(p, q, config)

    return result
