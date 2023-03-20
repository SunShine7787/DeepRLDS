#!/bin/bash

bsub -I -o q_share.log -b -q q_share -pr -n 3 -cgsp 64 -host_stack 4096 -share_size 11000 -cache_size 128 ./vina_reserve --manageNum 1
