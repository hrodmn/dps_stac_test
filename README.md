# DPS STAC Demo

Demonstrate how to produce STAC output in a DPS algorithm

## Motivation

Demonstrate how to create a STAC representation of a DPS algorithm's outputs.

## Sample Algorithm

This demo script reduces an image using rasterio and writes a STAC catalog + item.

### Usage (not in DPS)

```
python main.py -h
usage: main.py [-h] --input_file INPUT_FILE --output_dir OUTPUT_DIR --outsize OUTSIZE

Runs gdal_translate -outsize to reduce input size by n%

options:
  -h, --help            show this help message and exit
  --input_file INPUT_FILE
                        Input file to use
  --output_dir OUTPUT_DIR
                        Directory in which to save output
  --outsize OUTSIZE     Reduction size
```

For example:

```
main.py --input_file input_file.tif --output_dir output --outsize 25
```

### How to test algorithm before registration

Save the path to this repo:

```bash
repodir=$(pwd)
```

Create a temp working dir somewhere outside the code repository.

```bash
cd /tmp
```

Create the input directory and place the image in that directory

```bash
mkdir -p input
# Copy input file here
```

Run the [build-env.sh](build-env.sh) script from this temp directory to build custom env

```bash
bash ${repodir}/build-env.sh
```

Run the [run_gdal.sh](run_gdal.sh) script from this temp directory

```bash
bash ${repodir}/run.sh 50
```

If this script runs successfully then you are one step closer to running the algorithm on DPS.

### Next steps

- Register algorithm on DPS
- Submit Job
