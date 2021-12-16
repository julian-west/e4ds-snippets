# Mamba: Lightning Fast Python Package Management

> If you are using [conda](https://docs.conda.io/en/latest/) (Anaconda) for your package management. Stop right now and start using [mamba](https://github.com/mamba-org/mamba).


Mamba is a re-implementation of the `conda` package manager in C++ and comes with significant savings in time to resolve environments and download packages.

Mamba shares the same command line parser and package installation syntax as conda. Therefore, it doesn't require learning any new syntax. After installing, just replace the `conda` keyword with `mamba` 🚀

### Installation

If you already have [conda installed](https://engineeringfordatascience.com/posts/install_miniconda_from_the_command_line/), you can run the following command:

```
conda install mamba -n base -c conda-forge
```

### Installing packages with mamba

Use the same syntax as normal, just replace `conda` keyword with `mamba`. For example:

```
# create a new environment
mamba create -n testenv python=3.9 -y

# install some packages
mamba install jupyterlab voila ipywidgets xeus-python -y
```

---

## Performance Testing

There are five dockerfiles in this directory which download a number of Python packages. We can use these Dockerfiles to compare the time taken to download the packages:
- `conda` (Anaconda)
- `conda` (Miniconda)
- `mamba`
- `micromamba`
- `pip`

```
docker build -f mamba.Dockerfile .
```
