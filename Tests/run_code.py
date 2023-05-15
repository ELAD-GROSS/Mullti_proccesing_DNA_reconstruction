from test_time import *

def test_correctness(tests_num, strand_len):
    file = open("correctness.txt", "a")
    file.write(" success_rate \t\t average time\n\n")
    file.close()
    dict_data = {}
    total_successes = 0
    total_time = 0

    for i in range(tests_num):
        print(f"test num {i}")
        success, time_of_algorithm = run_parallel_algorithm(10, 2, 30, 20, strand_len, 30, 200)
        if success is not None:
            total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / 400) * 100
    avg_time = total_time / 400
    dict_data[strand_len] = (success_rate, avg_time)

    if success_rate is not None and avg_time is not None:
        save_data("correctness.txt", dict_data)


if __name__ == "__main__":
    # letter_amount = 2
    # frequency = 20
    # padding_size = 30
    general_test(algorithm_basic, 'basic.txt')
    # general_test(algorithm_ten_sections, '10_section.txt', letter_amount, frequency, padding_size)
    # general_test(algorithm_twenty_sections, '20_section.txt', letter_amount, frequency, padding_size)
    letter_amount = 3
    frequency = 20
    padding_size = 32
    # general_test(algorithm_ten_sections, '10_section.txt', letter_amount, frequency, padding_size)
    general_test(algorithm_twenty_sections, '20_section.txt', letter_amount, frequency, padding_size)
    test_correctness(400, 250_000)
