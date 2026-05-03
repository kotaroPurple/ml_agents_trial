import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_df() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n = 100
    return pd.DataFrame(
        {
            "MedInc": rng.uniform(1, 10, n),
            "HouseAge": rng.uniform(1, 50, n),
            "AveRooms": rng.uniform(3, 10, n),
            "AveBedrms": rng.uniform(1, 3, n),
            "Population": rng.uniform(100, 3000, n),
            "AveOccup": rng.uniform(1, 5, n),
            "Latitude": rng.uniform(32, 42, n),
            "Longitude": rng.uniform(-124, -114, n),
            "MedHouseVal": rng.uniform(0.5, 5.0, n),
        }
    )
