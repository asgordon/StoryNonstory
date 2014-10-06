
all: 
	gunzip en/en-model-UBT.txt.gz
	gunzip fa/fa-model-UBT.txt.gz
	gunzip zh/zh-model-UBT.txt.gz
	gunzip zh/cwsegment/combo.segmod.gz

compact:
	gzip en/en-model-UBT.txt
	gzip fa/fa-model-UBT.txt
	gzip zh/zh-model-UBT.txt
	gzip zh/cwsegment/combo.segmod


