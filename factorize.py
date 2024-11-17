from multiprocessing import Pool, cpu_count
from time import time


def factorize_number(n):
    factors = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            factors.append(i)
            if i != n // i:
                factors.append(n // i)
    return sorted(factors)


def factorize(*numbers):
    return [factorize_number(n) for n in numbers]


def parallel_factorize(*numbers):
    with Pool(cpu_count()) as pool:
        return pool.map(factorize_number, numbers)


if __name__ == "__main__":
    numbers = [128000, 255000, 9999999, 106510600]

    # Синхронне виконання
    start = time()
    results_sync = factorize(*numbers)
    end = time()
    print("Синхронне виконання:")
    for num, factors in zip(numbers, results_sync):
        print(f"{num}: {factors}")
    print(f"Час виконання: {end - start:.2f} сек\n")

    # Паралельне виконання
    start = time()
    results_parallel = parallel_factorize(*numbers)
    end = time()
    print("Паралельне виконання:")
    for num, factors in zip(numbers, results_parallel):
        print(f"{num}: {factors}")
    print(f"Час виконання: {end - start:.2f} сек\n")
