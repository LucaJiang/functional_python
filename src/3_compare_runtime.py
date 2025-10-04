# compare runtime of imperative vs functional
# usage: python3 src/3_compare_runtime.py --num-records 1000000 --iterations 5
import subprocess
import argparse
import os
import timeit
from typing import List


def run_script(script_name: str, num_records: int) -> None:
    """
    Run a script once.

    Args:
        script_name: Name of the script to run
        num_records: Number of records in the dataset
    """
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    result = subprocess.run(
        ["python", script_path, "-n", str(num_records)],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(__file__),
    )

    if result.returncode != 0:
        print(f"Error running {script_name}:")
        print(result.stderr)
        raise RuntimeError(f"Script {script_name} failed")


def benchmark_script(
    script_name: str, num_records: int, iterations: int = 10
) -> List[float]:
    """
    Benchmark a script by running it multiple times using timeit.

    Args:
        script_name: Name of the script to run
        num_records: Number of records in the dataset
        iterations: Number of times to run the script

    Returns:
        List of execution times
    """
    # Use timeit.repeat to run the script multiple times
    times = timeit.repeat(
        stmt=lambda: run_script(script_name, num_records),
        repeat=iterations,
        number=1,  # Run once per repeat
    )

    return times


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Compare runtime of imperative vs functional approaches"
    )
    parser.add_argument(
        "-n",
        "--num-records",
        type=int,
        default=100,
        help="Number of records in the dataset (default: 100)",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=10,
        help="Number of iterations for benchmarking (default: 10)",
    )
    args = parser.parse_args()

    num_records = args.num_records
    target_dataset = f"student_scores_{num_records}.csv"

    print("=" * 70)
    print("RUNTIME COMPARISON: Imperative vs Functional Programming")
    print("=" * 70)
    print(f"Dataset: {target_dataset}")
    print(f"Iterations: {args.iterations}")
    print()

    # Benchmark imperative approach
    print("Benchmarking Imperative Approach...")
    imp_times = benchmark_script(
        "1_imperative_summarize.py", num_records, args.iterations
    )
    imp_avg = sum(imp_times) / len(imp_times)
    imp_min = min(imp_times)
    imp_max = max(imp_times)

    # Benchmark functional approach
    print("Benchmarking Functional Approach...")
    fp_times = benchmark_script("2_fp_summarize.py", num_records, args.iterations)
    fp_avg = sum(fp_times) / len(fp_times)
    fp_min = min(fp_times)
    fp_max = max(fp_times)

    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print("\nImperative Approach:")
    print(f"  Average Time: {imp_avg*1000:.4f} ms")
    print(f"  Min Time:     {imp_min*1000:.4f} ms")
    print(f"  Max Time:     {imp_max*1000:.4f} ms")
    print(
        f"  Std Dev:      {(sum((t - imp_avg)**2 for t in imp_times) / len(imp_times))**0.5 * 1000:.4f} ms"
    )

    print("\nFunctional Approach:")
    print(f"  Average Time: {fp_avg*1000:.4f} ms")
    print(f"  Min Time:     {fp_min*1000:.4f} ms")
    print(f"  Max Time:     {fp_max*1000:.4f} ms")
    print(
        f"  Std Dev:      {(sum((t - fp_avg)**2 for t in fp_times) / len(fp_times))**0.5 * 1000:.4f} ms"
    )

    # Calculate speedup
    print("\n" + "=" * 70)
    print("COMPARISON")
    print("=" * 70)

    if imp_avg < fp_avg:
        speedup = fp_avg / imp_avg
        print(f"✓ Imperative is {speedup:.2f}x FASTER")
        print(f"  Time difference: {(fp_avg - imp_avg)*1000:.4f} ms")
    else:
        speedup = imp_avg / fp_avg
        print(f"✓ Functional is {speedup:.2f}x FASTER")
        print(f"  Time difference: {(imp_avg - fp_avg)*1000:.4f} ms")

    print()


if __name__ == "__main__":
    main()
