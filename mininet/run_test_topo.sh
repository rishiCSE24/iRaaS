sudo mn -c
sudo mn --custom ~/mytopo.py \
	--switch=ovsk,protocols=OpenFlow13 \
        --controller=remote,ip=192.168.200.101,port=6653 \
        --topo mytopo \
        --mac
