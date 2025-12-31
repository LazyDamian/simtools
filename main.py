import os
import numpy as np
import matplotlib.pyplot as plt
from src.game_logic import run_random_simulation
from src.game_logic_smart import run_smart_simulation
from src.monte_carlo import run_monte_carlo_simulation
from typing import Dict, Any

# --- Simulation Parameters ---
N_SIMULATIONS = 100000
BASE_SEED = 42


def save_histogram(random_data: np.ndarray, smart_data: np.ndarray, filename: str = "figures/comparison_histogram.png"):
    """
    Generates a comparative histogram of shots fired for two different strategies.
    Includes vertical indicators for mean values and saves the result as a PNG file.
    """
    os.makedirs("figures", exist_ok=True)
    plt.figure(figsize=(12, 7))

    # Statistical calculations for visualization
    avg_random = np.mean(random_data)
    avg_smart = np.mean(smart_data)

    # Create bins aligned with integer values to avoid binning artifacts
    all_data = np.concatenate([random_data, smart_data])
    bins = [i - 0.5 for i in range(int(min(all_data)), int(max(all_data)) + 2)]

    # Plotting distributions
    plt.hist(random_data, bins=bins, alpha=0.4, label='Random Strategy', color='red')
    plt.hist(smart_data, bins=bins, alpha=0.5, label='Smart AI', color='blue')

    # Add vertical indicators for average performance
    plt.axvline(avg_random, color='red', linestyle='dashed', linewidth=2, label=f'Avg Random: {avg_random:.2f}')
    plt.axvline(avg_smart, color='darkblue', linestyle='dashed', linewidth=2, label=f'Avg Smart: {avg_smart:.2f}')

    # Adjust Y-axis to provide space for labels above the plot bars
    current_max_y = plt.gca().get_ylim()[1]
    plt.ylim(0, current_max_y * 1.15)
    text_y_position = current_max_y * 1.05

    # Labeling mean values directly in the chart area
    plt.text(avg_random + 0.8, text_y_position, f'Avg: {avg_random:.2f}',
             color='red', fontweight='bold', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='red'))

    plt.text(avg_smart + 0.8, text_y_position, f'Avg: {avg_smart:.2f}',
             color='darkblue', fontweight='bold', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='darkblue'))

    # General chart formatting
    plt.title("Statistical Performance Comparison: Battleship Strategies", fontsize=14, pad=20)
    plt.xlabel("Number of Shots to Complete Game")
    plt.ylabel("Frequency (Occurrences)")
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def print_comparison_table(random_stats: Dict[str, Any], smart_stats: Dict[str, Any]):
    """
    Outputs a formatted statistical summary table to the console for performance analysis.
    """
    print("\n" + "=" * 65)
    print(f"{'STATISTICAL METRIC':<20} | {'RANDOM STRATEGY':<18} | {'SMART AI':<18}")
    print("-" * 65)

    metrics = [
        ('Average Shots', 'avg'),
        ('Minimum Shots', 'min'),
        ('Maximum Shots', 'max'),
        ('Standard Deviation', 'std_dev'),
        ('Variance', 'variance')
    ]

    for label, key in metrics:
        print(f"{label:<20} | {random_stats[key]:<18.2f} | {smart_stats[key]:<18.2f}")

    print("=" * 65 + "\n")


def main():
    """
    Main execution pipeline:
    1. Runs Monte Carlo simulations for both battleship strategies.
    2. Generates visual performance comparisons.
    3. Prints detailed statistical summaries.
    """
    print(f"Executing Battleship Monte Carlo Analysis ({N_SIMULATIONS} iterations)...")

    # Execute simulations using the multiprocessing engine
    res_random = run_monte_carlo_simulation(N_SIMULATIONS, run_random_simulation, BASE_SEED)
    res_smart = run_monte_carlo_simulation(N_SIMULATIONS, run_smart_simulation, BASE_SEED)

    # Data visualization
    save_histogram(res_random['raw_data'], res_smart['raw_data'])

    # Terminal output
    print_comparison_table(res_random, res_smart)
    print("Analysis complete. Visualizations saved to /figures.")


if __name__ == "__main__":
    main()