import logging
import multiprocessing
import time


def factorize(number, result_queue):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    result_queue.put(factors)


def factorize_all(*numbers):
    processes = []
    result_queue = multiprocessing.Queue()

    for num in numbers:
        process = multiprocessing.Process(target=factorize, args=(num, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    return results


if __name__ == "__main__":
    logging.basicConfig(format='%(processName)s - %(asctime)s - %(message)s', level=logging.DEBUG,
                        handlers=[logging.StreamHandler()])
    start = time.time()
    results = factorize_all(128, 255, 99999, 10651060)
    end = time.time()
    execution_time = end - start

    logging.debug(f'Результати:')
    for result in results:
        logging.debug(result)

    logging.debug(f'Час виконання функції: {execution_time}')
