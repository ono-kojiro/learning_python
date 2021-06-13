#set terminal png

set terminal postscript eps enhanced color
set output epsfile

set key left top
set xlabel "length"
set ylabel "bps"


set xtics ( \
	"4k" 4000, "8k" 8000, "16k" 16000, "32k" 32000, "64k" 64000, \
	"128k" 128000, "256k" 256000, "512k" 512000, "1024k" 1024000 )

plot datfile every :::0::0 using 4:($5/1000000) title "host read" with linespoints  lt 1, \
     datfile every :::1::1 using 4:($5/1000000) title "host write" with linespoints lt 2, \
     datfile every :::2::2 using 4:($5/1000000) title "kvm read" with linespoints lt 3, \
     datfile every :::3::3 using 4:($5/1000000) title "kvm write" with linespoints lt 4, \
     datfile every :::3::4 using 4:($5/1000000) title "qemu read" with linespoints lt 6, \
     datfile every :::5::5 using 4:($5/1000000) title "qemu write" with linespoints lt 7, \
     datfile every :::6::6 using 4:($5/1000000) title "virtualbox write" with linespoints lt 8, \
     datfile every :::7::7 using 4:($5/1000000) title "virtualbox write" with linespoints lt 9

