**Conferi o código. A descrição anterior precisa de alguns ajustes:** ele está configurado apenas para **ITA 49,9, combinado 660+808 nm**. As outras amostras exigem alterar os caminhos.

Ele também calcula **temperatura absoluta**, sem subtrair o baseline, e usa **desvio padrão populacional (`ddof=0`)**.

Use este texto no README:

```markdown
# Python Thermography Data Processing

This folder contains the Python script used to extract temperature measurements from exported thermography text files and generate CSV files and PNG plots.

## Input data

The script reads files from the folders listed in ROOT_FOLDERS, using natural filename ordering.

For each file, it extracts the last numeric value from the fifth line. If the file contains fewer than five lines, it extracts the last numeric value from the entire file.

Input folders must contain only the intended measurement files, because the script does not filter files by extension.

The current configuration processes three recordings from the ITA 49.9° specimen under combined 660+808 nm irradiation.

## Time axis

Time starts at zero, with a fixed interval defined by DT.

The current setting is DT = 0.111 seconds per measurement. This value must be checked against the acquisition interval.

## Outputs

For each recording, the script generates:
- A CSV file containing time and temperature.
- A PNG plot of temperature versus time.

For each group of three folders, it also generates:
- dado.csv, containing time, mean temperature and standard deviation.
- triplicata_media_dp.png, showing the mean curve with a shaded standard deviation band.

Recordings with different lengths are truncated to the shortest recording before calculating the mean and standard deviation.

Standard deviation is calculated using NumPy with ddof=0 (population standard deviation).

CSV files use semicolons as separators and commas as decimal separators. PNG plots are saved in the figuras subfolder.

## Requirements

- Python 3
- NumPy
- pandas
- Matplotlib

Install the dependencies with:

    pip install numpy pandas matplotlib

## How to run

1. Extract the input files if they are compressed.
2. Update ROOT_FOLDERS with the input folder paths on your computer.
3. List the three technical replicates consecutively.
4. Check DT.
5. Run the script.

The supplied paths use Windows-style separators.

## Scope and limitations

The script processes absolute temperature values. It does not subtract baseline temperature, calculate temperature rise, normalize cooling curves, or fit heating and cooling models.

Replicates are aligned by measurement index. The script does not detect irradiation onset or align recordings by experimental events.

Output files with the same names are overwritten when the script is run again.
```
