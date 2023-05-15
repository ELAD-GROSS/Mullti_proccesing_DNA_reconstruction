from Improvement.remove_meta_data import remove_meta_data
from Improvement.declassify_reads_improvement import declassify_reads
from Improvement.Utilities import *
from Improvement.Parallel_Algorithm_Improved import run_parallel_algorithm
from Improvement.find import find_longest


def main(sections_num, letters_amount, real_edge_len, frequency, strand_len, padding_size, read_size,
         read_lst):
    # declassify each read by its section
    four_pow = create_convert_list(read_size)
    try:
        # classifications = create_longest_classifications(letters_amount, sections_num)
        longest_classifications = find_longest(letters_amount)
        classifications = longest_classifications[0: sections_num]
        paddings_hash = create_paddings_hash(classifications, padding_size)
        paddings_to_classifications = {}

        for i in range(sections_num - 1):
            padding_letters = classifications[i][0] + classifications[i + 1]
            paddings_to_classifications[padding_letters] = [classifications[i], classifications[i + 1]]

    except ValueError:
        print("Can't create this many sections with only this amount of letters")
        exit(0)

    reads_by_sections = declassify_reads(read_lst, frequency, letters_amount, classifications,
                                         padding_size, paddings_hash, four_pow,
                                         paddings_to_classifications, sections_num)

    # run for each section Alex's algorithm
    # TODO: currently assuming that the strand_len / sections_num is a whole number,
    # change algorithm for unequal section lengths?
    strand_section_len_before = strand_len / sections_num
    special_section_length = get_section_size(strand_section_len_before, frequency, read_size, letters_amount)
    complete_sections = run_parallel_algorithm(reads_by_sections, read_size, real_edge_len, special_section_length,
                                               letters_amount)

    if complete_sections is None:
        return None
    # remove metadata from the solution
    strand_rebuilt = remove_meta_data(sections_num, complete_sections, frequency, letters_amount, read_size)

    return strand_rebuilt


def run_algorithm(sections_num, letters_amount, real_edge_len, frequency, strand_len, padding_size, read_size,
                        read_lst):
    # declassify each read by its section
    four_pow = create_convert_list(read_size)
    try:
        # classifications = create_longest_classifications(letters_amount, sections_num)
        longest_classifications = find_longest(letters_amount)
        classifications = longest_classifications[0: sections_num]
        paddings_hash = create_paddings_hash(classifications, padding_size)
        paddings_to_classifications = {}

        for i in range(sections_num - 1):
            padding_letters = classifications[i][0] + classifications[i + 1]
            paddings_to_classifications[padding_letters] = [classifications[i], classifications[i + 1]]

    except ValueError:
        print("Can't create this many sections with only this amount of letters")
        exit(0)
    # TODO: add documentation
    reads_by_sections, max_splits_arr = declassify_reads(read_lst, frequency, letters_amount, classifications,
                                                         padding_size, paddings_hash, four_pow,
                                                         paddings_to_classifications, sections_num)

    # run for each section Alex's algorithm
    # TODO: currently assuming that the strand_len / sections_num is a whole number,
    # change algorithm for unequal section lengths?
    strand_section_len_before = strand_len / sections_num
    special_section_length_no_padding = get_section_size(strand_section_len_before, frequency, letters_amount)
    complete_sections = run_parallel_algorithm(reads_by_sections, read_size, real_edge_len,
                                                                   special_section_length_no_padding, max_splits_arr)

    # for sec in complete_sections:
    #     print(sec)
    #     print("\n\n\n")
    if complete_sections is None:
        print("None, failed")
        return None
    # remove metadata from the solution


    strand_rebuilt = remove_meta_data(sections_num, complete_sections, frequency, letters_amount, read_size,
                                      max_splits_arr)
    print(special_section_length_no_padding)
    # print(strand_rebuilt)
    return strand_rebuilt
