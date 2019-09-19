#!/bin/sh
find /home/shopiot/log/ -mtime +10  -name "*.log" -exec rm -rf {} \; 