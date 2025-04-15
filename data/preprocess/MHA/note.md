MHA
- merge MHA 2024_09.01_11.30 with MHA 2024_12, in which both files have complete same format
- format: completely the same
-> so we have the complete WPV for MHA 2024/09/01 - 2024/12/31
1. **MHA 2024 09.01.24_12.31.csv** - break at Line 511, end at Line 680

- next merge `MHA 2024`
- format: 2 extra columns `Department/Office Incident Took Place` and `Assault Description`
-> concern about this file: it covers the entire 2024 time range, and we are not sure if it has any overlapping with other MHA datasets
-> given only 20 dp, less worried
2. **MHA 2024 09.01.24_12.31 - combine 2024.csv** - break at Line 680, end at Line 700

- next merge `MHA 2025.01`
- format: miss 1 column `Level of Care Needed` compared with MHA 2024_12
- assume equivalent to `Injury Assessed by`
3. **MHA 2024 09.01.24_2025.01.csv** - break at Line 700, end at Line 873

Leave the file `MHA 2024.08_10_dif_format.xlsx` unprocessed, which won't be involved in the MHA dataset, as the dp from 09-10/2024 may have potential overlapping.
- miss the column `Level of Care Needed`
-> given only 28dp, we should consider to incorporate into the overall dataset.

Overall, the merged data still needs further processing to unify numerical representations.