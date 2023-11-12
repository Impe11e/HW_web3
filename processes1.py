import logging
import time


def factorize(number):
    result = []
    for i in range(1, number + 1):
        if number % i == 0:
            result.append(i)
    return result


def factorize_all(*numbers):
    result = [factorize(number) for number in numbers]
    return result


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s', level=logging.DEBUG,
                        handlers=[logging.StreamHandler()])
    start = time.time()
    a, b, c, d = factorize_all(128, 255, 99999, 10651060)
    end = time.time()
    execution_time = end - start

    logging.debug(f'{a},\n{b},\n{c},\n{d}\n')

    logging.debug(f'Час виконання функції: {execution_time}')
