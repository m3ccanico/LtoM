#!/bin/bash
gdalwarp -te 1515430.0 5204444.0 1529280.0 5213944.0 join.tif 00.tif
tiff2pdf 00.tif -o 00.pdf
convert -font helvetica -fill '#0085be' -pointsize 8 -density 300 -undercolor '#ffffff80' -rotate 90 -annotate +10+125 '15,16,000' -annotate +10+361 '15,17,000' -annotate +10+597 '15,18,000' -annotate +10+833 '15,19,000' -annotate +10+1070 '15,20,000' -annotate +10+1306 '15,21,000' -annotate +10+1542 '15,22,000' -annotate +10+1778 '15,23,000' -annotate +10+2014 '15,24,000' -annotate +10+2251 '15,25,000' -annotate +10+2487 '15,26,000' -annotate +10+2723 '15,27,000' -annotate +10+2959 '15,28,000' -annotate +10+3196 '15,29,000' -rotate -90 00.pdf 00.pdf
convert -font helvetica -fill '#0085be' -pointsize 8 -density 300 -undercolor '#ffffff80' -annotate +10+2103 '52,05,000' -annotate +10+1867 '52,06,000' -annotate +10+1630 '52,07,000' -annotate +10+1394 '52,08,000' -annotate +10+1158 '52,09,000' -annotate +10+922 '52,10,000' -annotate +10+685 '52,11,000' -annotate +10+449 '52,12,000' -annotate +10+213 '52,13,000' 00.pdf 00.pdf
convert -density 300 -stroke '#0085be' -strokewidth 3 -font helvetica -fill '#0085be' -pointsize 8 -undercolor '#ffffff80' -draw 'line 2953,472 2953,118' -draw 'line 2953,472 3080,118' -strokewidth 1 -annotate +2929+94 'GN' -annotate +3056+94 'MN' -annotate +2993+177 '21°' 00.pdf 00.pdf
gdalwarp -te 1516802.0 5211967.0 1530652.0 5221467.0 join.tif 01.tif
tiff2pdf 01.tif -o 01.pdf
convert -font helvetica -fill '#0085be' -pointsize 8 -density 300 -undercolor '#ffffff80' -rotate 90 -annotate +10+273 '15,18,000' -annotate +10+509 '15,19,000' -annotate +10+745 '15,20,000' -annotate +10+982 '15,21,000' -annotate +10+1218 '15,22,000' -annotate +10+1454 '15,23,000' -annotate +10+1690 '15,24,000' -annotate +10+1927 '15,25,000' -annotate +10+2163 '15,26,000' -annotate +10+2399 '15,27,000' -annotate +10+2635 '15,28,000' -annotate +10+2871 '15,29,000' -annotate +10+3108 '15,30,000' -rotate -90 01.pdf 01.pdf
convert -font helvetica -fill '#0085be' -pointsize 8 -density 300 -undercolor '#ffffff80' -annotate +10+1990 '52,13,000' -annotate +10+1754 '52,14,000' -annotate +10+1518 '52,15,000' -annotate +10+1281 '52,16,000' -annotate +10+1045 '52,17,000' -annotate +10+809 '52,18,000' -annotate +10+573 '52,19,000' -annotate +10+337 '52,20,000' -annotate +10+100 '52,21,000' 01.pdf 01.pdf
convert -density 300 -stroke '#0085be' -strokewidth 3 -font helvetica -fill '#0085be' -pointsize 8 -undercolor '#ffffff80' -draw 'line 2953,472 2953,118' -draw 'line 2953,472 3080,118' -strokewidth 1 -annotate +2929+94 'GN' -annotate +3056+94 'MN' -annotate +2993+177 '21°' 01.pdf 01.pdf
convert -density 300 00.pdf 01.pdf map.pdf
rm 00.pdf 00.tif 01.pdf 01.tif 

