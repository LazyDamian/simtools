import numpy as np
import time
import multiprocessing
from numpy.random import SeedSequence, PCG64, Generator
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, Tuple, List, Dict, Any

# Simulation function now expects a ready-to-use Generator
SimFunc = Callable[[Generator], int]


def _worker_task(args: Tuple[SimFunc, SeedSequence]) -> int:
    """
    Helper function to initialize the RNG within each separate process
    and run the simulation.
    """
    func, seed_seq = args
    # Create the actual technical Generator object here
    rng = Generator(PCG64(seed_seq))
    return func(rng=rng)


def run_monte_carlo_simulation(
        n_simulations: int,
        sim_function: SimFunc,
        base_seed: int = 42
) -> Dict[str, Any]:
    """
    Executes simulations in parallel using SeedSequence for independent streams.
    """
    print(f"Starting Simulation: {n_simulations} games (Parallel) ...")
    start_time = time.time()
    n_cores = multiprocessing.cpu_count()

    # Generate reproducible seeds for every individual game
    master_seq = SeedSequence(base_seed)
    child_sequences = master_seq.spawn(n_simulations)
    tasks = [(sim_function, seq) for seq in child_sequences]

    with ProcessPoolExecutor(max_workers=n_cores) as executor:
        chunk = max(1, n_simulations // (n_cores * 5))
        results_list = list(executor.map(_worker_task, tasks, chunksize=chunk))

    results = np.array(results_list)
    duration = time.time() - start_time
    print(f"Simulation finished. Duration: {round(duration, 2)}s.")

    return {
        'avg': np.mean(results),
        'median': np.median(results),
        'variance': np.var(results),
        'std_dev': np.std(results),
        'min': np.min(results),
        'max': np.max(results),
        'duration': round(duration, 4),
    }