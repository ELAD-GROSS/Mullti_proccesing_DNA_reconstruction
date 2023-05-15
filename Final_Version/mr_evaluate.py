from Final_Version.declassify_reads_improvement import find_repetitive_letters
import Tests.Utilities_Test as ut
from Final_Version.add_meta_data import classify_strand
from Final_Version.find import find_longest

# notice that checking split reads is not needed
# because it is a negligible amount of reads


sections_amount = 10
real_edge_len = 30

NUM_TESTS = 10 ** 3


def get_dict_from_strand(sections_list, read_size):
    new_dict = dict()
    for section_idx in range(len(sections_list)):
        section = sections_list[section_idx]
        for i in range(len(section) - read_size):
            curr_read = section[i:i + read_size]
            new_dict[curr_read] = section_idx
    return new_dict


def finding_num_of_bad_reads(reads, reads_dict: dict):
    sum_bad_reads = 0

    for section_idx in range(len(reads)):
        reads_of_section_idx = reads[section_idx]

        for read in reads_of_section_idx:
            if read in reads_dict:
                sum_bad_reads += reads_dict[read] != section_idx

    return sum_bad_reads + len(reads[-1])


def get_growth_rate_percent(len_original, len_new_no_padding, num_section, padding_size):
    new_len = (num_section - 1) * padding_size + len_new_no_padding
    return ((new_len - len_original) / len_original) * 100


def find_candidate_classifications(all_reads, letters_amount, frequency, classifications, section_num):
    list_to_return = [[] for _ in range(section_num + 1)]
    for section_list in all_reads:
        for read in section_list:
            candidate = find_repetitive_letters(read, letters_amount, frequency, classifications)
            if candidate != "":
                list_to_return[classifications.index(candidate)].append(read)
            else:
                list_to_return[section_num].append(read)
    return list_to_return


def finding_avg_miss_rate_of_declassified_reads(strand_len, frequencies, letter_amounts_to_padding_size, read_size,
                                                string_input=""):
    """
    :return: the average miss rate of declassified reads
    """
    data_to_return = dict()
    if string_input != "":
        original_str = string_input
    else:
        original_str = ut.generate_strand(strand_len)
    section_len = len(original_str) // sections_amount

    original_sections = [original_str[i:i + section_len] for i in range(0, len(original_str), section_len)]

    for letters_amount, padding_size in letter_amounts_to_padding_size.items():
        for frequency in frequencies:
            total_reads = 0
            total_bad_reads = 0
            growth_rate_percent = 0
            longest_classifications = find_longest(letters_amount)  # for letter_amount equals 4 it will not work
            classifications = longest_classifications[0: sections_amount]

            print("letters_amount: ", letters_amount, "frequency: ", frequency)
            for i in range(NUM_TESTS):

                classified_reads = [[] for _ in range(sections_amount)]
                classified_sections = []
                for section_index in range(sections_amount):
                    classified_sections.append(
                        classify_strand(original_sections[section_index], 1, frequency,
                                        [classifications[section_index]],
                                        padding_size))
                    classified_reads[section_index] = ut.generate_reads(classified_sections[section_index],
                                                                        len(classified_sections[section_index]),
                                                                        read_size)
                classified_length = len(''.join(classified_sections))
                reads_dict = get_dict_from_strand(classified_sections, read_size)

                # percent of growth
                growth_rate_percent = get_growth_rate_percent(len(original_str), classified_length, sections_amount,
                                                              padding_size)
                sum_list = [len(classified_reads[i]) for i in range(0, len(classified_reads))]
                total_reads += sum(sum_list)

                reads_declassified = find_candidate_classifications(classified_reads, letters_amount, frequency,
                                                                    classifications, sections_amount)

                total_bad_reads += finding_num_of_bad_reads(reads_declassified, reads_dict)
            print(data_to_return)
            miss_rate = total_bad_reads / total_reads
            data_to_return[growth_rate_percent] = [miss_rate, frequency, letters_amount]
    return data_to_return
