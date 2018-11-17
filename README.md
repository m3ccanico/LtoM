# LtoM

Uses a line (defined by two coordinates) and generate A4 maps that cover the defined line.

## Run

```bash
./LtoM.py 1507000 5250000 1501000 5239000 BV21_GeoTifv1-06.tif
```

## FAQ

Error:
```
convert: not authorized `/tmp/magick-z4igycWL' @ error/constitute.c/ReadImage/45 3.
convert: missing an image filename `out.png' @ error/convert.c/ConvertImageComma 
```

Edit `/etc/ImageMagick-6/policy.xml` and change:

```
...
  <policy domain="coder" rights="read|write" pattern="PDF" />
...
```