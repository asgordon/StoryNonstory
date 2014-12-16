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

Lang    | Prec  | Rec   | F1    | Acc   | +train | -train
--------|-------|-------|-------|-------|--------|-------
English | 0.775 | 0.325 | 0.458 | 0.922 | 403    | 3579
Farsi   | 0.489 | 0.151 | 0.230 | 0.972 | 446    | 15931
Chinese | 0.572 | 0.217 | 0.314 | 0.925 | 457    | 5379

Precision, Recall, and F1 scores are for "story" class.

References
----------
This work is based on the research presented in the following two conference papers. 
* Gordon, A. and Swanson, R. (2009) Identifying Personal Stories in Millions of Weblog Entries. Third International Conference on Weblogs and Social Media, Data Challenge Workshop, San Jose, CA, May 20, 2009. http://people.ict.usc.edu/~gordon/publications/ICWSM09-DCW.PDF
* Gordon, A., Huangfu, L., Sagae, K., Mao, W., and Chen, W. (2013) Identifying Personal Narratives in Chinese Weblog Posts. The 2013 Intelligent Narrative Technologies Workshop (INT6), October 14-15, 2013, Boston, MA. http://people.ict.usc.edu/~gordon/publications/INT13.PDF
