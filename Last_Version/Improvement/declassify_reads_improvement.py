from Improvement.Utilities import *

NO_FULL_PADDING = -1


def find_repetitive_letters(read, letters_amount, frequency, classifications):
    for i in range(0, frequency + letters_amount):
        candidate = read[i: i + letters_amount]
        if candidate not in classifications:
            continue
        was_repetitive = True

        for j in range(i + frequency + letters_amount, len(read), frequency + letters_amount):
            temp = read[j:j + letters_amount]

            if len(temp) != len(candidate):
                break
            if temp != candidate:
                was_repetitive = False
                break

        if was_repetitive:
            return candidate
    return ""


def find_full_padding(read, padding_size, paddings_hash, four_pow):
    temp_hash = full_hash(read=read, pos=0, length=padding_size)
    for pos in range(1, len(read) - padding_size + 1):
        if temp_hash in paddings_hash:
            if read[pos - 1:pos - 1 + padding_size] in paddings_hash[temp_hash]:
                return pos - 1

        temp_hash = shift_right_hash(read, pos, padding_size, temp_hash, four_pow)
    return NO_FULL_PADDING


def is_padding_at_start(read, letters_amount, freq):
    padding_partial = read[0:letters_amount + 1] * (freq // (letters_amount + 1))
    padding_partial += read[0:freq % (letters_amount + 1)]
    return padding_partial == read[0:freq]


def declassify_with_padding(read, freq, padding_size, paddings_hash, letters_amount, four_pow):
    # can be two cases: either the padding is somewhere in the middle, in which case it is in full length,
    # or it will be partially cut in the beginning or the end.
    # If it's in the middle,
    # we'll check if every padding_length combo of letters is one of possible paddings in the next function:
    padding_start = find_full_padding(read, padding_size, paddings_hash, four_pow)

    if padding_start != NO_FULL_PADDING:
        return read[padding_start: padding_start + letters_amount + 1], (True, padding_start)
    # otherwise, the padding is partial and in either the beginning or the end
    else:
        is_at_start = is_padding_at_start(read, letters_amount, freq)

        if is_at_start:
            return read[0:letters_amount + 1], (False, 0)
        else:
            return read[-letters_amount - 1:], (False, -1)


def split_read(read, letters, padding_pos_start, pad_to_candidates, padding_size):
    read_prev_section, read_next_section = None, None

    [classification_before, classification_after] = pad_to_candidates[letters]

    padding_for_prev = create_padding_forward(len(read) - padding_pos_start, classification_before,
                                              classification_after)
    padding_for_next = create_padding_backward(padding_pos_start, classification_before, classification_after)

    if padding_pos_start != 0:
        read_prev_section = read[0:padding_pos_start] + padding_for_prev

    if padding_pos_start != len(read) - padding_size:
        read_next_section = padding_for_next + read[padding_pos_start:]

    return read_prev_section, read_next_section


# data1 + ACTACTACTACT + data2
#  prev  = data1 + ACT....
#  padd + padding data2 ->   CTACTAC T ACTACTACTACT data2

def declassify_read(read, freq, letters_amount, classifications, padding_size, paddings_hash, four_pow,
                    pad_to_candidates):
    candidate_letters = find_repetitive_letters(read, letters_amount, freq, classifications)
    # check if the function find_repetitive_letters succeeded
    if candidate_letters != "":
        return candidate_letters, NO_FULL_PADDING

    # otherwise, there is padding that foiled the function
    padding_letters, (is_full_padding, padding_start_pos) = declassify_with_padding(read, freq, padding_size,
                                                                                    paddings_hash, letters_amount,
                                                                                    four_pow)
    rotated_str = padding_letters
    for i in range(len(padding_letters)):
        if rotated_str in pad_to_candidates:
            break
        rotated_str = padding_letters[i:] + padding_letters[:i]

    if not is_full_padding:
        if padding_start_pos == 0:
            # not full padding and padding at start, return second classification of dict
            return pad_to_candidates[rotated_str][1], NO_FULL_PADDING
        else:
            return pad_to_candidates[rotated_str][0], NO_FULL_PADDING
    else:
        # there is full padding
        return rotated_str, padding_start_pos


def declassify_reads(reads, freq, letters_amount, classifications, padding_size, paddings_hash, four_pow,
                     pad_to_candidates, num_of_sections):
    read_prev_section = None
    read_next_section = None

    maxes_arr_indexes = [[0, 0] for _ in range(num_of_sections)]
    maxes_arr_reads = [["", ""] for _ in range(num_of_sections)]


    reads_by_sections = [[] for _ in range(num_of_sections)]
    letters_to_section = {classifications[i]: i for i in range(0, len(classifications))}

    for read in reads:
        letters, padding_pos_start = declassify_read(read, freq, letters_amount, classifications, padding_size,
                                                     paddings_hash, four_pow, pad_to_candidates)

        if padding_pos_start == NO_FULL_PADDING:
            section_num = letters_to_section[letters]
            reads_by_sections[section_num].append(read)

        else:
            # full padding, need to split read
            section_num = letters_to_section[pad_to_candidates[letters][1]]
            read_prev_section, read_next_section = split_read(read, letters, padding_pos_start, pad_to_candidates,
                                                              padding_size)
            if read_prev_section is not None and padding_pos_start > maxes_arr_indexes[section_num - 1][1]:
                maxes_arr_reads[section_num - 1][1] = read_prev_section
                maxes_arr_indexes[section_num - 1][1] = padding_pos_start
            if read_next_section is not None and len(read) - padding_pos_start - padding_size > \
                    maxes_arr_indexes[section_num][0]:
                maxes_arr_reads[section_num][0] = read_next_section
                maxes_arr_indexes[section_num][0] = len(read) - padding_pos_start - padding_size

    for section_num in range(num_of_sections):
        if maxes_arr_reads[section_num][0] != "":
            reads_by_sections[section_num].append(maxes_arr_reads[section_num][0])

        if maxes_arr_reads[section_num][1] != "":
            reads_by_sections[section_num].append(maxes_arr_reads[section_num][1])

    return reads_by_sections, maxes_arr_indexes

