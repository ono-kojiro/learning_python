#set terminal png

set terminal pdf color font ',10'
set output pdffile

set key left top
set logscale x 2
set xrange [2048:1048576000]
set format x "10^{%L}"
set xlabel "block size"
set ylabel "band width (M/s)"


#set xtics ( \
#	"4K" 4000, "8K" 8000, "16K" 16000, "32K" 32000, "64K" 64000, \
#	"128K" 128000, "256K" 256000, "512K" 512000, \
#	"1M" 1024000, "2M" 2048000, "4M" 4096000, "8M" 8192000, \
#	"16M" 16384000, "32M" 32768000, "64M" 65536000, "128M" 131072000, \
#	"256M" 262144000, "512M" 524288000 \
#)

set xtics ( \
	"4Ki"     4096, \
	"8Ki"     8192, \
	"16Ki"    16384, \
	"32Ki"    32768, \
	"64Ki"    65536, \
	"128Ki"   131072, \
	"256Ki"   262144, \
	"512Ki"   524288 \
)

plot datfile every :::0::0 using 5:($6/1000000) title "read" with lp lt 1, \
     datfile every :::1::1 using 5:($6/1000000) title "write" with lp lt 2

