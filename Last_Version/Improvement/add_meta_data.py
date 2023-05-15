import textwrap
import math
from Improvement.Utilities import create_padding_forward


def classify_strand(strand, sections_amount, frequency, classifications, padding_size):
    """
    The function receives a strand and adds meta-data in order to classify each section of the strand.
    This is done by two ways:
     1) Every "frequency" amount of letters a classification of the section is added to the data.
        For example, frequency=3, strand=AGCTACGTACGTA and classification of "GG" will lead to
        AGGGCTGGACGGGTGGTAGGCGGGTAGG
     2) Between every section a padding of "read_size" length is added to the strand so a read
        will have only exactly one section of data.
    :param padding_size: The size of the padding that will be added as meta-data.
    :param classifications: The different classifications in order for the sections
    :param padding: The padding to put between every section
    :param strand: the original strand without classification
    :param sections_amount: how many sections to divide the strand
    :param frequency: how often to insert classifications of section in data
    :return: The new strand with both ways of meta-data included
    """
    # if padding size is not a multiple of the letters_amount, this will not work!
    if padding_size % (len(classifications[0]) + 1) != 0:
        raise ValueError(f"The padding size must be a multiple of letters_amount + 1")

    sections_list = textwrap.wrap(strand, width=int(math.ceil(len(strand) / sections_amount)), break_long_words=True)

    for section_num in range(0, sections_amount):
        sub_sections = textwrap.wrap(sections_list[section_num], width=frequency, break_long_words=True)
        section_without_first_classification = \
            "".join(sub_section + classifications[section_num] for sub_section in sub_sections)

        if section_num != 0:
            padding = create_padding_forward(padding_size, classifications[section_num - 1],
                                             classifications[section_num])
            section = "".join((padding, classifications[section_num], section_without_first_classification))
        else:
            section = "".join((classifications[section_num], section_without_first_classification))
        sections_list[section_num] = section

    return "".join(sections_list)
