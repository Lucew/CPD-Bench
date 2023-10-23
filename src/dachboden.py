def load_dataset(filename):
    """ Load a CPDBench dataset """
    with open(filename, "r") as fp:
        data = json.load(fp)

    if data["time"]["index"] != list(range(0, data["n_obs"])):
        raise NotImplementedError(
            "Time series with non-consecutive time axis are not yet supported."
        )

    mat = np.zeros((data["n_obs"], data["n_dim"]))
    for j, series in enumerate(data["series"]):
        mat[:, j] = series["raw"]

    # We normalize to avoid numerical errors.
    mat = (mat - np.nanmean(mat, axis=0)) / np.sqrt(np.nanvar(mat, axis=0, ddof=1))

    np.save("../data/apple.npy", mat)

    return data, mat