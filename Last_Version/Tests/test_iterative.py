import Utilities_Test as ut
from Parallel_Algorithm.classify_strand_sections import classify_strand
from Parallel_Algorithm.classifying_no_parallel import final_algorithm
import time

NUM_TESTS = 10


def run_iterative_algorithm(strand_size, read_size, real_edge_len, freq, letters_amount, classifications, g_freq,
                            sections_num, strand=""):
    if strand == "":
        original_strand = ut.generate_strand(strand_size)
    else:
        original_strand = strand

    classified_strand = classify_strand(original_strand, sections_num, freq, classifications, g_freq, read_size)
    # full cover
    iterative_algorithm_reads = ut.generate_reads(classified_strand, len(classified_strand), read_size)

    iterative_time = time.time()
    iterative_strand = final_algorithm(sections_num, letters_amount, classifications, real_edge_len, freq, strand_size,
                                       g_freq, read_size, iterative_algorithm_reads)
    iterative_time = time.time() - iterative_time
    iterative_algorithm_success = iterative_strand is not None and original_strand == iterative_strand
    if iterative_algorithm_success:
        print(original_strand)
        print(iterative_strand)
    return iterative_algorithm_success, iterative_time


def algorithm_ten_sections(strand_size):
    total_successes = 0
    total_time = 0

    sections_num = 10
    read_size = 200
    real_edge_len = 20
    freq = 10
    letters_amount = 5

    # classifications = ["AC", "AT", "CA", "CT", "CG", "CC", "GT", "GC", "GG", "TA"]
    classifications = ut.create_classification(sections_num + 10, letters_amount)
    new_classifications = []
    for c in classifications:
        if not (c[3:] == 'AG' or c[3:] == 'GA'):
            if len(new_classifications) < sections_num:
                new_classifications.append(c)

    print(new_classifications)
    g_freq = 25

    for _ in range(NUM_TESTS):
        success, time_of_algorithm = run_iterative_algorithm(strand_size, read_size, real_edge_len, freq,
                                                             letters_amount,
                                                             new_classifications, g_freq, sections_num)
        if success is not None:
            total_successes += success
        total_time += time_of_algorithm
        print(success)
        print(time_of_algorithm)
        print()
    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


def algorithm_twenty_sections(strand_size):
    total_successes = 0
    total_time = 0

    sections_num = 20
    read_size = 200
    real_edge_len = 20
    freq = 10
    letters_amount = 3
    classifications = ut.create_classification(sections_num, letters_amount)
    g_freq = 25

    for i in range(NUM_TESTS):
        i += 1
        print(f"test num {i}")
        success, time_of_algorithm = run_iterative_algorithm(strand_size, read_size, real_edge_len, freq,
                                                             letters_amount,
                                                             classifications, g_freq, sections_num)

        print(success)
        print(time_of_algorithm)
        if success is not None:
            total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    print(success_rate)
    print(avg_time)
    return success_rate, avg_time


if __name__ == '__main__':
    strand_len = 1_000_000
    success_rate_ten_sections, avg_time_ten_sections = algorithm_ten_sections(strand_len)
    print(f"strand length: {strand_len}", end=", ")
    print(f"success rate: {success_rate_ten_sections} , avg time: {avg_time_ten_sections}")
# algorithm_ten_sections(250_000)
# algorithm_twenty_sections(250_000)

# with open('iterative_10_sections') as f:
#     lines = f.read().splitlines()
#
# lst = [float(lines[i]) for i in range(len(lines)) if i % 3 == 2]
# success_lst = [bool(lines[i]) for i in range(len(lines)) if i % 3 == 1]
# print(success_lst)
# print(sum(success_lst))
# print(lst)
# print(len(lst))
# print(sum(lst) / len(lst))
