from mr_evaluate import *


def main():
    file_name = "strand.txt"
    strand_file = open(file_name, "w")

    strand_len = 500_000
    read_size = 200
    letter_amounts_to_padding_size = {4: 30, 5: 30}
    frequencies = [i for i in range(10, 51, 5)]

    growth_rate_dict = finding_avg_miss_rate_of_declassified_reads(strand_len, frequencies,
                                                                   letter_amounts_to_padding_size, read_size)
    print(growth_rate_dict)

    # write to file the dict
    strand_file.write(str(growth_rate_dict))
    strand_file.close()


if __name__ == "__main__":
    main()
