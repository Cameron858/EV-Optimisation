from ev_optimisation.vehicle import GenerationResult
import numpy as np
import pandas as pd


def result_to_json(result: dict[int, GenerationResult]) -> dict:
    """
    Convert a dictionary of GenerationResult objects into a compact JSON representation.

    This function concatenates the pandas DataFrames from each GenerationResult,
    applies space-saving transformations (rounding, type conversions, and column drops),
    and returns a JSON-serializable structure using the "split" orientation.

    Parameters
    ----------
    result : dict[int, GenerationResult]
        A dictionary mapping generation indices to their corresponding GenerationResult objects.

    Returns
    -------
    dict
        A JSON-serializable dictionary in the "split" orientation containing the
        concatenated and compressed results.
        Keys include "columns", "index", and "data".

    Notes
    -----
    The following optimizations are applied to reduce JSON size:
    - All numeric values are rounded to 2 decimal places.
    - The "Crowding Distance" column is dropped.
    - The "Range" column is further rounded to the nearest integer.
    - The "Front" column is cast to uint8.
    """
    result_dfs = []
    for generation_result in result.values():
        result_dfs.append(generation_result.to_pandas())
    df = pd.concat(result_dfs)

    # space saving
    df = df.round(2)
    df = df.drop("Crowding Distance", axis=1)
    df["Range"] = df["Range"].round(0)
    df["Front"] = df["Front"].astype(np.uint8)

    return df.reset_index(drop=True).to_json(orient="split")
