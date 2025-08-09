import csv

with (
    open("../english_5.txt", "r") as d,
    open("../trim_5_words.csv", "r") as in_freq,
    open("../dict_5_words.csv", "w") as out_freq,
):
    ifl = csv.reader(in_freq)
    ofl = csv.writer(out_freq)
    l = d.readlines()
    l = [s.strip() for s in l]

    for line in ifl:
        if line[0] in l:
            ofl.writerow(line)
