StoryNonstory
=============

Identify personal stories in English, Farsi, or Chinese plaintext.

Input should be a plain text file containing documents that you wish to classify, one per line. Farsi and Chinese should be encoded with the (standard) UTF-8 character encodings. 

Output will be "story" or "nonstory" on one line for every line in the input file.


Installing
----------

Model files are compressed using gzip, and need to be unzipped before using. From a linux command line prompt, type:

  make


Using
-----

For English:

  cat input.txt | python en/enFeatures.py | python classify.py en/en-model-UBT.txt > output.txt

For Farsi:

  cat input.txt | python fa/faFeatures.py | python classify.py fa/fa-model-UBT.txt > output.txt

For Chinese:

  cat input.txt | perl zh/cwsegment/cwsegment.pl combo.segmod | python zh/zhFeatures.py | python classify.py zh/zh-model-UBT.txt > output.txt


Expected accuracy
-----------------

Lang		Prec	Rec	F1	Acc	+train	-train
English		0.775	0.325	0.458	0.922	403	3579
Farsi		0.489	0.151	0.230	0.972	446	15931
Chinese		0.572	0.217	0.314	0.925	457	5379

Precision, Recall, and F1 scores are for "story" class.