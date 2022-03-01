#set terminal png

#set terminal postscript eps enhanced color
set terminal pdf color font ',10'
set output pdffile

set key left top
set logscale x 2
set xrange [1024:134217728]
set format x "10^{%L}"
set xlabel "block size"
set ylabel "band width (MByte/s)"


set xtics ( \
	"4K" 4096, "8K" 8192, "16K" 16384, "32K" 32768, "64K" 65536, \
	"128K" 131072, "256K" 262144, "512K" 524288, \
    "1M" 1048576, \
    "2M" 2097152, \
    "4M" 4194304, \
    "8M" 8388608, \
    "16M" 16777216, \
    "32M" 33554432, \
    "64M" 67108864, \
)

plot datfile every :::0::0 using 3:($4/1000000) title "native read" with linespoints  lt 1, \
     datfile every :::1::1 using 3:($4/1000000) title "native write" with linespoints lt 2

