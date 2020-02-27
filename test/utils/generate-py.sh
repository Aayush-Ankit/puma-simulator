# Copy this file to compiler test folder where the .npy files are generated.
# Update SIMULATOR_PATH value and execute it.

SIMULATOR_PATH=" " # simulator root path

if [[ $SIMULATOR_PATH == "" ]] ; then
    print "Error, missing simulator path."
    exit
fi


PYTHON=python2

for g in *.puma; do
    echo $g
    #Parse tile and core ids
    dataset="$( cut -d '-' -f 1 <<< "$g" )"
    #echo $dataset
    tileid=$(echo $g | grep -o -E 'tile[0-9]+' | head -1)

    if [[ $g == *"core"* ]]; then
        #coredid=$(echo $g | cut -d " " -f $N)
        coreid=$(echo "${g: -6}")
        coreid="$( cut -d '.' -f 1 <<< "$coreid" )"
        filename='core_imem'$coreid
    else
        filename='tile_imem'
    fi
    mkdir -p $dataset/$tileid
    dir=$dataset/$tileid
    f=$dataset/$tileid/$g

    echo "" > $f.py
    echo "import sys, os" >> $f.py
    echo "import numpy as np" >> $f.py
    echo "import math" >> $f.py
    echo "sys.path.insert (0, '$SIMULATOR_PATH/include/')" >> $f.py
    echo "sys.path.insert (0, '$SIMULATOR_PATH/src/')" >> $f.py
    echo "sys.path.insert (0, '$SIMULATOR_PATH/')" >> $f.py
    echo "from data_convert import *" >> $f.py
    echo "from instrn_proto import *" >> $f.py
    echo "from tile_instrn_proto import *" >> $f.py
    echo "dict_temp = {}" >> $f.py
    echo "dict_list = []" >> $f.py
    while read line
    do
        echo "i_temp = i_$line" >> $f.py
        echo "dict_list.append(i_temp.copy())" >> $f.py
    done < $g
    echo "filename = '$dir/$filename.npy'" >> $f.py
    echo "np.save(filename, dict_list)" >> $f.py
    $PYTHON $f.py
done


cp input.py $dataset/input.py

echo $dataset
cd $dataset
$PYTHON input.py

if [[ $1 == *"-c"* ]]; then 
    $PYTHON $SIMULATOR_PATH/Security/encrypter.py $2 $PWD
    rm -r tile*
fi

if [[ $1 == *"-a"*  ]]; then
    $PYTHON $SIMULATOR_PATH/Security/generateMAC.py $2 $PWD
fi

cd ..
$PYTHON populate.py
