import Utilities_Test as ut
from Improvement.find import find_longest
from Improvement.main import run_algorithm
from Original_Algorithm.algorithm import final_algorithm
from Improvement.add_meta_data import classify_strand
from Improvement import declassify_reads_improvement


def test():
    # def main(sections_num, letters_amount, real_edge_len, frequency, strand_len, padding_size, read_size,
    #          read_lst):
    sections_num = 4
    letters_amount = 3
    real_edge_len = 20
    frequency = 10
    strand_len = 100_000
    padding_size = 30
    read_size = 100

    sections_num = 10
    letters_amount = 2
    real_edge_len = 20
    frequency = 20
    strand_len = 1000000
    padding_size = 30
    read_size = 200



    orig_str = ut.generate_strand(strand_len)

    # orig_reads = ut.generate_reads(orig_str, strand_len, read_size)
    # candidate_basic = final_algorithm(strand_len, read_size, real_edge_len, orig_reads)
    #
    # if orig_str == candidate_basic:
    #     print("control worked")

    longest_classifications = find_longest(letters_amount)
    classifications = longest_classifications[0: sections_num]
    classified_str = classify_strand(orig_str, sections_num, frequency, classifications, padding_size)
    # print(orig_str)
    classified_reads = ut.generate_reads(classified_str, len(classified_str), read_size)
    print(f"reads amount: {len(classified_reads)}")
    # print(classified_str)
    # print("\n\n\n")
    candidate_improve = run_algorithm(sections_num, letters_amount, real_edge_len, frequency, strand_len, padding_size,
                             read_size, read_lst=classified_reads)
    # print(f"original: {orig_str}")
    # print(f"candidate: {candidate_improve}")
    if candidate_improve == orig_str:
        print("test worked!")

def test_specific():
    read = "CCACGAGCGGCAACAGCGCTAAGCTCAGAGGATCTGACAGTGATGATGTCAATTGCCCCCCCACTAGCAAATTCATTGCGGAATACACCTATGCCCGCAG"
    classifications = ['AC', 'CT', 'TT', 'TG', 'GC', 'CG', 'GA', 'AT', 'TA', 'AG']
    four_pow = [1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304, 16777216, 67108864, 268435456, 73741818, 294967272, 179869082, 219476325, 377905297, 11621179, 46484716, 185938864, 243755453, 475021809, 400087227, 100348899, 401395596, 105582375, 422329500, 189317991, 257271961, 29087838, 116351352, 465405408, 361621623, 446486486, 285945935, 143783734, 75134933, 300539732, 202158922, 308635685, 234542734, 438170933, 252683723, 10734886, 42939544, 171758176, 187032701, 248130801, 492523201, 470092795, 380371171, 21484675, 85938700, 343754800, 375019194, 76767, 307068, 1228272, 4913088, 19652352, 78609408, 314437632, 257750522, 31002082, 124008328, 496033312, 484133239, 436532947, 246131779, 484527113, 438108443, 252433763, 9735046, 38940184, 155760736, 123042941, 492171764, 468687047, 374748179, 498992710, 495970831, 483883315, 435533251, 242132995, 468531977, 374127899, 496511590, 486046351, 444185395, 276741571, 106966278, 427865112, 211460439, 345841753, 383367006, 33468015, 133872060]
    paddings_hash = {132146444: ['ACTACTACTACTACTACTACTACTACTACT'], 228077107: ['CTTCTTCTTCTTCTTCTTCTTCTTCTTCTT'], 456154214: ['TTGTTGTTGTTGTTGTTGTTGTTGTTGTTG'], 290335325: ['TGCTGCTGCTGCTGCTGCTGCTGCTGCTGC'], 360223551: ['GCGGCGGCGGCGGCGGCGGCGGCGGCGGCG'], 95930663: ['CGACGACGACGACGACGACGACGACGACGA'], 160732217: ['GATGATGATGATGATGATGATGATGATGAT'], 297965333: ['ATAATAATAATAATAATAATAATAATAATA'], 158188881: ['TAGTAGTAGTAGTAGTAGTAGTAGTAGTAG']}
    pad_to_candidates = {'ACT': ['AC', 'CT'], 'CTT': ['CT', 'TT'], 'TTG': ['TT', 'TG'], 'TGC': ['TG', 'GC'], 'GCG': ['GC', 'CG'], 'CGA': ['CG', 'GA'], 'GAT': ['GA', 'AT'], 'ATA': ['AT', 'TA'], 'TAG': ['TA', 'AG']}
    declassify_reads_improvement.declassify_read(read, 10, 2, classifications, 30, paddings_hash, four_pow, pad_to_candidates)

if __name__ == "__main__":
    test()
