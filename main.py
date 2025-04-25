import argparse
from pathlib import Path

import rasterio
from pystac import (
    Catalog,
    CatalogType,
)
from rasterio.enums import Resampling
from rio_stac.stac import create_stac_item


def resize_geotiff_by_percent(input_path: str, output_path: str, percent: int | float):
    """
    Resize a GeoTIFF file by a percentage of its original size.

    Parameters:
    -----------
    input_path : str
        Path to the input GeoTIFF file
    output_path : str
        Path where the resized GeoTIFF will be saved
    percent : float
        Percentage to resize (e.g., 50.0 for half size, 200.0 for double size)
    """
    scale_factor = percent / 100.0

    with rasterio.open(input_path) as src:
        width = int(src.width * scale_factor)
        height = int(src.height * scale_factor)

        transform = src.transform * src.transform.scale(
            (src.width / width), (src.height / height)
        )

        profile = src.profile
        profile.update({"height": height, "width": width, "transform": transform})

        data = src.read(
            out_shape=(src.count, height, width),
            resampling=Resampling.nearest,
        )

        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(data)

    print(f"Resized {input_path} to {percent}% of original size at {output_path}")


if __name__ == "__main__":
    parse = argparse.ArgumentParser(
        description="Runs gdal_translate -outsize to reduce input size by n%"
    )
    parse.add_argument("--input_file", help="Input file to use", required=True)
    parse.add_argument(
        "--output_dir", help="Directory in which to save output", required=True
    )
    parse.add_argument("--outsize", help="Reduction size", required=True, type=int)
    args = parse.parse_args()

    output_dir = Path(args.output_dir)
    output_file = str(output_dir / f"resized_{args.outsize}.tif")

    resize_geotiff_by_percent(
        input_path=args.input_file, output_path=output_file, percent=args.outsize
    )

    print("writing STAC metadata")
    catalog = Catalog(
        id="DPS",
        description="DPS",
        catalog_type=CatalogType.SELF_CONTAINED,
    )
    item = create_stac_item(
        source=output_file,
        id=Path(args.input_file).stem,
        # override asset_href to be relative to the output directory
        asset_href=str(output_file).replace(f"{args.output_dir}/", ""),
        with_proj=True,
    )
    item.set_self_href(f"{args.output_dir}/item.json")

    catalog.add_item(item)
    item.make_asset_hrefs_relative()

    catalog.normalize_and_save(
        root_href=str(output_dir),
        catalog_type=CatalogType.SELF_CONTAINED,
    )
