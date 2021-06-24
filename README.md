# comparing-football-players
Using statistics and machine learning to compare football players

## Get data and merge dataframes
```
# Get data from FBREF
python -m src.get_data

# Merge dataframes
python -m src.merge_data
```

## Calcule PCA and save dataframes
```
# Calcule PCA and save transformed dataset
python -m src.calcule_pca
```

TO DO:
- Create inference script
- Add DVC to manage the pipeline and data
- Create web app
