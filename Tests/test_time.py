import time

# from Tests import Utilities_Test as ut
import Utilities_Test as ut
from Final_Version import find_longest
from Final_Version import run_algorithm
from Final_Version import classify_strand
from Original_Algorithm_Alex import algorithm

NUM_TESTS = 25


def run_original_algorithm(strand_size, read_size, real_edge_len):
    original_strand = ut.generate_strand(strand_size)
    # full cover
    regular_algorithm_reads = ut.generate_reads(original_strand, strand_size, read_size)

    non_parallel_time = time.time()
    regular_algorithm_result = algorithm.final_algorithm(strand_size, read_size, real_edge_len,
                                                         regular_algorithm_reads)
    non_parallel_time = time.time() - non_parallel_time
    regular_algorithm_success = regular_algorithm_result != None and regular_algorithm_result[0] == original_strand
    return regular_algorithm_success, non_parallel_time


def run_parallel_algorithm(sections_num, letters_amount, real_edge_len, frequency, strand_len, padding_size, read_size):
    orig_str = ut.generate_strand(strand_len)

    longest_classifications = find_longest(letters_amount)
    classifications = longest_classifications[0: sections_num]
    classified_str = classify_strand(orig_str, sections_num, frequency, classifications, padding_size)
    classified_reads = ut.generate_reads(classified_str, len(classified_str), read_size)

    start_time = time.time()
    candidate_improve = run_algorithm(sections_num, letters_amount, real_edge_len, frequency, strand_len, padding_size,
                                      read_size, read_lst=classified_reads)

    parallel_time = time.time() - start_time

    parallel_algorithm_success = candidate_improve is not None and orig_str == candidate_improve
    return parallel_algorithm_success, parallel_time


def algorithm_basic(strand_size):
    total_successes = 0
    total_time = 0
    read_size = 200
    real_edge_len = 20
    i = 0

    for _ in range(NUM_TESTS):
        i += 1
        print(f"test num {i}")
        success, time_of_algorithm = run_original_algorithm(strand_size, read_size, real_edge_len)
        total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


def algorithm_ten_sections(strand_len, letters_amount, frequency, padding_size):
    sections_num = 10
    # letters_amount = 2
    real_edge_len = 30
    # frequency = 20
    # padding_size = 30
    read_size = 200

    total_time = 0
    total_successes = 0
    for i in range(NUM_TESTS):

        print(f"test num {i + 1}")

        success, time_of_algorithm = run_parallel_algorithm(sections_num, letters_amount, real_edge_len, frequency,
                                                            strand_len, padding_size, read_size)
        if success is not None:
            total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


def algorithm_twenty_sections(strand_len, letters_amount, frequency, padding_size):
    sections_num = 20
    # letters_amount = 3
    real_edge_len = 30
    # frequency = 20
    # padding_size = 32
    read_size = 200

    total_time = 0
    total_successes = 0
    for i in range(NUM_TESTS):

        print(f"test num {i + 1}")

        success, time_of_algorithm = run_parallel_algorithm(sections_num, letters_amount, real_edge_len, frequency,
                                                            strand_len, padding_size, read_size)
        if success is not None:
            total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


def save_data(file_name, dict_data):
    file = open(file_name, "a")
    file.write("strand length \t\t success_rate \t\t average time\n\n")
    for strand_len, (success_rate, avg_time) in dict_data.items():
        print(f"{strand_len}\t\t\t\t\t{success_rate}\t\t\t\t\t{avg_time}\n")
        file.write(f"{strand_len}\t\t\t\t\t{success_rate}\t\t\t\t\t{avg_time}\n")
    file.close()


# this is the main function it gets an algorithm that its only parameter is strand size
# returns success rate and avg time
# see basic algorithm for example
def general_test(algorithm_test, file_name, letter_amount=0, frequency=0, padding_size=0):
    print(f'{algorithm_test.__name__}\n')

    file = open("basic.txt", "a")
    file.write("strand length \t\t success_rate \t\t average time\n\n")
    file.close()

    dict_data = {}

    # for strand_len in range(250_000, 1_500_001, 250_000):
    for strand_len in range(250_000, 1_000_001, 250_000):
        print(f"length currently is {strand_len}")

        if letter_amount == 0:
            success_rate, avg_time = algorithm_test(strand_len)
        else:
            success_rate, avg_time = algorithm_test(strand_len, letter_amount, frequency, padding_size)

        dict_data[strand_len] = (success_rate, avg_time)
        if success_rate is not None and avg_time is not None:
            save_data(file_name, dict_data)

    return dict_data
