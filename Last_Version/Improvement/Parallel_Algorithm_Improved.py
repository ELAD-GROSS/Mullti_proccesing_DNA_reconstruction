from multiprocessing import Process, Manager
from Improvement.algorithm import final_algorithm
from Improvement.Utilities import get_section_size, create_convert_list
from Improvement.declassify_reads_improvement import declassify_reads
from Improvement.find import find_longest

is_failed = -1


def run_section_algorithm(section_reads_lst: list, section_len, read_size,
                          real_edge_length,
                          complete_sections_dict, section):
    candidate_results = final_algorithm(section_len, read_size, real_edge_length, section_reads_lst)

    if candidate_results is None or len(candidate_results) != 1:
        complete_sections_dict[is_failed] = 1

    else:
        # if there is more than one item the algorithm fails
        complete_sections_dict[section] = next(iter(candidate_results))


def run_parallel_algorithm(reads_lst, read_size, real_edge_length, section_len_no_padding, max_splits_arr):
    """
    :param paddings_by_sections: A list of sections, in each item has a list of padding position
           (weather starting at beginning of read, end of read or has no padding)
    :param reads_lst: Each item of the list is a list of reads that is classified by a section
    :param read_size: The size of a read
    :param real_edge_length: A parameter for the original algorithm
    :param special_sections_length: The length of the first/last sections including classifications.
           In order to get the other sections' lengths, add read_size - letters_amount to this
    :param letters_amount: Amount of letters used for classifying the string to sections
    :return: If successful, then a list containing the sections of the original string, otherwise the list will have
             Nones in it which will indicate that the algorithm failed in at least one of the parallel sections
    """
    processes = []
    section_amount = len(reads_lst)
    manager = Manager()
    shared_dict = manager.dict()
    complete_sections = []

    for section in range(section_amount):
        # if 0 < section < section_amount - 1:
        #     # TODO: subtract by letters_amount
        #     section_len = special_sections_length + read_size
        #
        # else:
        #     section_len = special_sections_length
        #
        # p = Process(target=run_section_algorithm,
        #             args=(
        #                 reads_lst[section], int(section_len), read_size,
        #                 real_edge_length, shared_dict, section))
        # processes.append(p)
        section_len = section_len_no_padding

        if section != section_amount - 1:
            # adding padding length for end of section
            section_len += read_size - max_splits_arr[section][1]
        if section != 0:
            # adding padding length for start of section
            section_len += read_size - max_splits_arr[section][0]
        p = Process(target=run_section_algorithm,
                    args=(reads_lst[section], int(section_len), read_size,
                          real_edge_length, shared_dict, section))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    if is_failed in shared_dict.keys():
        return None

    for section_num in range(section_amount):
        complete_sections.append(shared_dict[section_num])
    return complete_sections


def run_parallel_algorithm_not_really_parallel(reads_lst, read_size, real_edge_length,
                                               section_len_no_padding, max_splits_arr):
    """
    :param reads_lst: Each item of the list is a list of reads that is classified by a section
    :param read_size: The size of a read
    :param real_edge_length: A parameter for the original algorithm
    :param section_len_no_padding: The length of the first/last sections including classifications.
           In order to get the other sections' lengths, add read_size - letters_amount to this
    :param max_splits_arr:
    :return: If successful, then a list containing the sections of the original string, otherwise the list will have
             Nones in it which will indicate that the algorithm failed in at least one of the parallel sections
    """
    # section_before padding section_after
    # section_before big_padding
    # big_padding section_after
    section_amount = len(reads_lst)
    shared_dict = dict()
    complete_sections = []

    for section in range(section_amount):
        section_len = section_len_no_padding

        if section != section_amount - 1:
            # adding padding length for end of section
            section_len += read_size - max_splits_arr[section][1]
        if section != 0:
            # adding padding length for start of section
            section_len += read_size - max_splits_arr[section][0]

        run_section_algorithm(reads_lst[section], int(section_len), read_size,
                              real_edge_length, shared_dict, section)

    if is_failed in shared_dict.keys():
        return None

    for section_num in range(section_amount):
        complete_sections.append(shared_dict[section_num])
    return complete_sections
