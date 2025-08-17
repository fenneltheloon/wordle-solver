For each word, sort remaining words into buckets
depending on the result that they would get from guessing the guessed word

(GGGGG is a bucket, GBGBG is another, etc.)

Calculate the mean size of each bucket and standard deviation in bucket size

Get a metric that corresponds to how different the distribution is from the
flat distribution: we want uniform distribution of remaining words in all 3 ** 5
bins.

For each bin, measure difference between actual count and expected count

Expected count = total remaining words / number of bins (3 ** wordlength)
