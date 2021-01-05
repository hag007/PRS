cut -f 1,2,4 hgTable.txt | awk '{gsub("^chr",""); print $0}' | sed 's/\t/_/'
