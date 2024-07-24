from from_file_to_pd_code      import from_file_to_pd_code
from from_pd_code_to_knot_name import from_pd_code_to_knot_name

def khovanov_indexer_pipeline(che_file: str) -> list[str]:
    pd_code   = from_file_to_pd_code(che_file)
    knotnames = from_pd_code_to_knot_name(pd_code)
    return knotnames

if __name__ == "__main__":
    import os
    DIRNOW      = os.path.dirname(os.path.abspath(__file__))
    SAMPLE_FILE = os.path.join(DIRNOW, 
                               "che_data_to_pd_code", "src", "che_data_to_spatial_coord", "src", "data.random_knot_widened_L1000_K0_melt_limit_1")
    assert os.path.isfile(SAMPLE_FILE)
    print(khovanov_indexer_pipeline(SAMPLE_FILE))