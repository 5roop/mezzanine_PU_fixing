
exbs = ["Rog-Art-J-Gvecg-P500001.exb","Rog-Art-J-Gvecg-P500002.exb","Rog-Art-J-Gvecg-P500014.exb","Rog-Art-J-Gvecg-P500016.exb","Rog-Art-J-Gvecg-P500021.exb","Rog-Art-J-Gvecg-P500026.exb","Rog-Art-J-Gvecg-P500028.exb","Rog-Art-J-Gvecg-P500034.exb","Rog-Art-J-Gvecg-P500037.exb","Rog-Art-J-Gvecg-P500042.exb","Rog-Art-J-Gvecg-P500046.exb","Rog-Art-J-Gvecg-P500048.exb","Rog-Art-J-Gvecg-P500051.exb","Rog-Art-J-Gvecg-P500054.exb","Rog-Art-J-Gvecg-P500063.exb","Rog-Art-J-Gvecg-P500064.exb","Rog-Art-J-Gvecg-P580002.exb","Rog-Art-J-Gvecg-P580003.exb","Rog-Art-J-Gvecg-P580009.exb","Rog-Art-J-Gvecg-P580023.exb","Rog-Art-J-Gvecg-P580041.exb","Rog-Art-J-Gvecg-P580047.exb","Rog-Art-J-Gvecg-P580051.exb","Rog-Art-N-G5013-P600007.exb","Rog-Art-N-G5014-P600007.exb","Rog-Art-N-G5019-P600012.exb","Rog-Art-N-G5020-P600012.exb","Rog-Art-N-G5025-P600021.exb","Rog-Art-N-G5025-P600022.exb","Rog-Art-N-G5026-P600021.exb","Rog-Art-N-G5035-P600034.exb","Rog-Art-N-G5036-P600034.exb","Rog-Art-N-G5043-P600044.exb","Rog-Art-N-G5044-P600044.exb","Rog-Art-N-G5053-P600052.exb","Rog-Art-N-G5054-P600052.exb","Rog-Art-N-G5082-P600080.exb","Rog-Art-N-G5083-P600080.exb","Rog-Art-N-G5097-P600096.exb","Rog-Art-N-G6001-P600102.exb","Rog-Art-N-G6007-P600702.exb","Rog-Art-N-G6012-P601201.exb","Rog-Art-N-G6031-P603102.exb","Rog-Art-N-G6043-P604301.exb","Rog-Art-N-G6047-P604702.exb","Rog-Art-N-G6060-P606001.exb","Rog-Art-N-G6083-P608301.exb","Rog-Art-N-G6100-P610002.exb","Rog-Art-N-G6103-P610302.exb","Rog-Art-N-G6112-P611202.exb","Rog-Art-N-G6116-P611601.exb","Rog-Art-P-G7001-P700192.exb","Rog-Art-P-G7002-P700444.exb","Rog-Art-P-G7036-P701111.exb","Rog-Art-P-G7065-P701064.exb","Rog-Art-P-G7155-P700259.exb","Rog-Art-P-G7165-P700926.exb",]

rule unzip:
    output: expand("indata/{i}", i=exbs)
    shell:
        """
        cd indata;
        unzip ../Rog*.zip
        cp ../manual_corrections/* .
        """


rule do_one:
    input: "indata/{file}"
    output: "outdata/{file}"
    script: "do_one.py"


rule gather:
    default_target: True
    input: expand("outdata/{i}", i=exbs)
    output: "Rog-Art-PU-peter-apr2025.zip"
    shell:
        """cd outdata
        zip {output} *.exb;
        mv *.zip .."""
