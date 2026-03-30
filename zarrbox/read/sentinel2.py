"""
Reader implementation for Sentinel-2 data.

This module should:
- Implement Sentinel-2-specific parsing logic
- Handle multi-resolution bands (10m, 20m, 60m)
- Use configuration from source-data/sentinel2/config.json

Responsibilities:
- Band selection and resampling (if needed)
- Metadata extraction
- SAFE format handling
"""
from base import BaseReader
from pathlib import Path
import rioxarray


class Sentinel2Reader(BaseReader):

    def read_data(self, pansharpen=False):
        """
        Reads Sentinel-2 scene and returns a Dataset with DataArrays for each resolution.
        """

        # Ensure path points to a folder inside GRANULE 
        assert self.path.parts[-2] == "GRANULE", (
            "please provide the path to the specific scene like "
            "'/S2A_MSIL1C_20260306T103041_N0512_R108_T31TGM_20260306T154507.SAFE/GRANULE/L1C_T31TGM_A055904_20260306T103041'"
        )

        image_folder = self.path / "IMG_DATA"

        # adapt scen_name to match the naming of the .jp2 files 
        scene_name = self.path.parts[-1]
        parts = scene_name.split("_")
        scene_name = f"{parts[1]}_{parts[3]}"

        # Bands grouped by native resolution, in dict
        bands_by_res = {
            "10m": ['B02', 'B03', 'B04', 'B08'],
            "20m": ['B05', 'B06', 'B07', 'B8A', 'B11', 'B12'],
            "60m": ['B01', 'B09', 'B10']
        }

        full_data = xr.Dataset()

        for res, bands in bands_by_res.items():
            layer_list = []
            for band in bands:
                file_path = image_folder / f"{scene_name}_{band}.jp2"

                if not file_path.exists():
                    print(f"WARNING: Band {band} not found!")
                    continue

                # Open raster lazily
                band_data = rioxarray.open_rasterio(file_path, chunks={"x": 1830, "y": 1830})
                band_data = band_data.assign_coords(band=[band])
                layer_list.append(band_data)

            if not layer_list:
                print(f"WARNING: No bands found for resolution {res}, skipping.")
                continue

            # Stack bands along 'band' dimension
            res_cube = xr.concat(layer_list, dim="band", join="exact")
            full_data[res] = res_cube

        if pansharpen:
            full_data = self.pansharpen(full_data)
        return full_data

    def pansharpen(self, ds: xr.Dataset) -> xr.DataArray:   
        """
        Interpolates 20m and 60m bands to 10m resolution and returns a DataCube
        """
    
        # Reference 10m DataArray
        da_10m = ds["10m"]

        resampled_layers = [da_10m]  

        # Resample 20m bands
        if "20m" in ds:
            da_20m = ds["20m"].rio.reproject_match(
                da_10m,
                resampling=Resampling.bilinear  # or 'nearest' if categorical
            )
            resampled_layers.append(da_20m)

        # Resample 60m bands
        if "60m" in ds:
            da_60m = ds["60m"].rio.reproject_match(
                da_10m,
                resampling=Resampling.bilinear
            )
            resampled_layers.append(da_60m)

        # Concatenate all bands along 'band' dimension
        full_cube = xr.concat(resampled_layers, dim="band", join="exact")

        # Ensure band names are unique / preserved
        band_names = []
        for layer in resampled_layers:
            band_names.extend(layer.band.values.tolist())
        full_cube = full_cube.assign_coords(band=band_names)

        return full_cube

    def read_metadata(self):
        """(Source Specific: Reads metadata from source-specific metadata format to unified)"""
        raise NotImplementedError #for now as TBD




