import argparse
import subprocess
from pathlib import Path

from pystac import (
    Catalog,
    CatalogType,
    Collection,
    Extent,
    SpatialExtent,
    TemporalExtent,
)
from rio_stac.stac import create_stac_item


def gdal_translate(input_filename, output_filename, reduction_percent):
    gdal_cmd = [
        "gdal_translate",
        "-outsize",
        f"{reduction_percent}%",
        f"{reduction_percent}%",
        input_filename,
        output_filename,
    ]
    proc = subprocess.Popen(gdal_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = proc.communicate()
    print(out)
    return proc.returncode, output_filename


if __name__ == "__main__":
    parse = argparse.ArgumentParser(
        description="Runs gdal_translate -outsize to reduce input size by n%"
    )
    parse.add_argument("--input_file", help="Input file to use", required=True)
    parse.add_argument("--outsize", help="Reduction size", required=True)
    parse.add_argument("--collection_id", help="STAC collection ID", required=True)
    args = parse.parse_args()

    output_file = f"output/resized_{args.outsize}.tif"
    exit_code, output = gdal_translate(args.input_file, output_file, args.outsize)

    if exit_code != 0:
        print(f"gdal_translate failed with a non-zero exit code: {exit_code}")
        exit(exit_code)

    print("writing STAC metadata")
    catalog = Catalog(
        id="DPS",
        description="DPS",
        catalog_type=CatalogType.SELF_CONTAINED,
    )
    collection = Collection(
        id=args.collection_id,
        description="description",
        title=args.collection_id,
        extent=Extent(
            spatial=SpatialExtent(bboxes=[[-180, -90, 180, 90]]),
            temporal=TemporalExtent([[None, None]]),
        ),
    )
    catalog.add_child(collection)
    item = create_stac_item(
        source=output_file,
        collection=collection.id,
        id=Path(args.input_file).stem,
        # override asset_href to be relative to the output directory
        asset_href=output_file.replace("output/", ""),
        with_proj=True,
    )
    item.set_self_href("output/item.json")

    collection.add_item(item)
    item.make_asset_hrefs_relative()

    catalog.normalize_and_save(
        root_href="output/",
        catalog_type=CatalogType.SELF_CONTAINED,
    )
