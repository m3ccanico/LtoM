# LtoM

Line to Map (LtoM) is a crude Python script that helps generation A4 maps based on the publically available Geo-TIFFs in New Zealand.

It uses a line (defined by two coordinates) and a Geo-TIFF file as the input to generates a shell script that cuts landscape A4 pages out along the line with some overlap between them, adds coordinates, and the declination.

## Run

### Join the Map Sheets

First identify and download the Geo-TIFF files with http://www.nztopomaps.com/ and combine them into a single Geo-TIFF:

```sh
gdalwarp --config GDLA_CACHEMAX 3000 -wm 3000 BU20_GeoTifv1-05.tif BU21_GeoTifv1-03.tif BU22_GeoTifv1-05.tif BU23_GeoTifv1-06.tif BV20_GeoTifv1-05.tif BV21_GeoTifv1-08.tif join.tif
```

### Generate the Map

Then use http://www.nztopomaps.com/ to identify the coordinates of the start and end point and run the script:

```bash
uv run LtoM.py 1491717 5264078 1547868 5283227 join.tif > run.sh
chmod +x run.sh
./run.sh
```

## FAQ

### Error

```sh
convert: not authorized `/tmp/magick-z4igycWL' @ error/constitute.c/ReadImage/45 3.
convert: missing an image filename `out.png' @ error/convert.c/ConvertImageComma 
```

Edit `/etc/ImageMagick-6/policy.xml` and change:

```sh
...
  <policy domain="coder" rights="read|write" pattern="PDF" />
...
```
