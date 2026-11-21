
# Surface Heating and Cooling in Ex Vivo Human Skin under 660 nm, 808 nm, and Combined Irradiation

## 1. Dataset description

This repository is intended to provide experimental thermographic and colorimetric data supporting the manuscript:

**Surface Heating and Cooling in Ex Vivo Human Skin under 660 nm, 808 nm, and Combined Irradiation: An Exploratory Study of Associations with Skin Color**

The study investigated the association between skin color, assessed using the Individual Typology Angle (ITA), and surface heating and post-irradiation cooling during photobiomodulation (PBM) in five independent ex vivo human abdominal skin specimens.

The dataset is organized by specimen and irradiation protocol to facilitate the identification, verification, and reproduction of the experimental analyses.

## 2. Skin specimens

Five independent human skin specimens obtained from different donors were investigated.

Skin color was characterized using the CIELAB color space and the Individual Typology Angle (ITA).

| Specimen | ITA (°), mean ± SD | Skin typology |
|---|---|---|
| 1 | 54.2 ± 5.8 | Light |
| 2 | 49.9 ± 8.3 | Light |
| 3 | 16.3 ± 3.4 | Tan |
| 4 | -15.7 ± 1.0 | Brown |
| 5 | -33.8 ± 5.4 | Dark |

Colorimetric measurements were performed using a Delta Vista 450G colorimeter (DeltaColor, Brazil).

Three measurements were obtained at different locations on each specimen. ITA was calculated individually from the corresponding L* and b* coordinates and subsequently averaged.

ITA is a colorimetric descriptor of skin color and does not directly quantify melanin concentration.

## 3. Irradiation protocols

All specimens were irradiated using a Therapy EC laser device (DMC, Brazil).

Three irradiation protocols were investigated:

| Protocol | Optical power | Irradiation time | Total energy |
|---|---|---|---|
| 660 nm | 100 mW | 60 s | 6 J |
| 808 nm | 100 mW | 60 s | 6 J |
| Simultaneous 660 + 808 nm | 200 mW (100 mW per wavelength) | 30 s | 6 J (3 J per wavelength) |

Each protocol was performed in triplicate at adjacent, non-overlapping irradiation sites within each specimen.

The experimental design comprised:

- Five independent biological specimens (n = 5).
- Three irradiation protocols per specimen.
- Three technical replicates per irradiation protocol (n = 3).

The technical replicates were not considered independent biological observations.

## 4. Thermographic acquisition

Surface temperature was monitored using a Fluke Ti400 infrared camera (Fluke, USA).

The thermographic acquisition parameters were:

- Image resolution: 320 × 240 pixels.
- Acquisition rate: approximately 9 Hz.
- Thermal sensitivity: approximately 0.1 °C.
- Emissivity: 0.98.
- Pre-irradiation baseline: 15 s.
- Irradiation period: 30 or 60 s, depending on the protocol.
- Post-irradiation cooling monitoring: 100 s.

Thermographic sequences were analyzed using Fluke SmartView software.

For each recording, the pixel corresponding to the highest observed surface temperature within the irradiated region was identified retrospectively.

The spatial coordinates of this pixel were then kept fixed throughout the thermographic sequence, including baseline, irradiation, and cooling periods.

Temperature extraction was based on a single fixed pixel rather than a multipixel region of interest.

## 5. Temperature extraction and data processing

The experimental data were processed sequentially using Fluke SmartView, Python, Microsoft Excel, and Origin software.

### 5.1. Fluke SmartView

Thermographic recordings acquired with the Fluke Ti400 camera were initially analyzed using Fluke SmartView software.

Temperature measurements from the selected fixed pixel were extracted from the thermographic sequences.

The exported temperature records were subsequently used as input data for Python processing.

### 5.2. Python processing

The temperature records exported from SmartView were processed using a custom Python script (`main.py`) executed in the Spyder environment.

The Python script:

1. Reads the previously exported temperature records.
2. Organizes the records in chronological order.
3. Extracts the numerical temperature values.
4. Assigns time values using a sampling interval of 0.111 s.
5. Generates individual CSV files containing time and absolute temperature.

The CSV files use the following columns:

- Time (s).
- Temperature (°C).

The script was reused for the experimental recordings by updating the input folder paths corresponding to each thermographic sequence.

### 5.3. Microsoft Excel

The individual CSV files generated using Python were imported into Microsoft Excel.

For each specimen and irradiation protocol, the temperature measurements from the three technical replicates were organized into separate columns.

Mean temperature values and standard deviations were calculated from the three technical replicates.

Temperature increase was calculated relative to the pre-irradiation baseline:

**ΔT = T - T0**

where:

- T is the measured absolute temperature (°C).
- T0 is the mean temperature during the 15 s pre-irradiation baseline (°C).
- ΔT is the temperature increase relative to baseline (°C).

The maximum temperature increase was defined as ΔTmax.

### 5.4. Origin software

The processed Excel data were imported into Origin software (OriginLab Corporation, Northampton, MA, USA).

Origin was used for:

- Graph preparation.
- Visualization of mean temperature curves.
- Representation of experimental variability.
- Mathematical fitting of heating curves.
- Mathematical fitting of post-irradiation cooling curves.
- Visualization of normalized cooling curves.

Post-irradiation cooling was also expressed as the dimensionless ratio:

**ΔT / ΔTmax**

## 6. Repository organization

Experimental data are organized by specimen ITA value and irradiation protocol.

The intended repository structure is:

```text
skin-pigmentation-thermal-response/
|
|-- README.md
|
|-- 01_raw_data/
|   |
|   |-- ITA_54.2/
|   |   |-- 660nm/
|   |   |-- 808nm/
|   |   |-- 660_808nm/
|   |
|   |-- ITA_49.9/
|   |   |-- 660nm/
|   |   |-- 808nm/
|   |   |-- 660_808nm/
|   |
|   |-- ITA_16.3/
|   |   |-- 660nm/
|   |   |-- 808nm/
|   |   |-- 660_808nm/
|   |
|   |-- ITA_minus_15.7/
|   |   |-- 660nm/
|   |   |-- 808nm/
|   |   |-- 660_808nm/
|   |
|   |-- ITA_minus_33.8/
|       |-- 660nm/
|       |-- 808nm/
|       |-- 660_808nm/
|
|-- 02_processed_data/
|
|-- 03_figures/
|
|-- 04_analysis_code/
|   |-- main.py
```

### 6.1. Temperature data

The `01_raw_data` directory is intended to contain the individual temperature-time CSV files exported by the Python script, organized by specimen and irradiation protocol.

These files represent temperature data extracted from thermographic recordings and are not the original Fluke thermographic files.

### 6.2. Processed data

The `02_processed_data` directory is intended to contain Excel spreadsheets used to calculate mean temperatures, standard deviations, baseline-corrected temperature increases, and other derived results.

### 6.3. Figures and mathematical fitting

The `03_figures` directory is intended to contain data and files associated with the experimental graphs and mathematical fitting performed using Origin, where available.

### 6.4. Analysis code

The `04_analysis_code` directory is intended to contain the Python script used to process the temperature records exported from SmartView.

The same processing script was used for different recordings by modifying the corresponding input paths.

## 7. Mathematical modeling

### 7.1. Heating

Heating curves were described using an empirical logarithmic model:

**ΔT(t) = a × log(1 + t/b)**

where:

- ΔT(t) is the temperature increase (°C).
- t is time (s).
- a is a fitted amplitude-related parameter (°C).
- b is a fitted characteristic time parameter (s).

### 7.2. Cooling

Post-irradiation cooling curves were described using a three-term exponential decay model:

**ΔT(t) = A1 × exp(-t/t1) + A2 × exp(-t/t2) + A3 × exp(-t/t3)**

where A1, A2, and A3 are fitted amplitude coefficients and t1, t2, and t3 are fitted characteristic time constants.

The models were fitted using Origin software and were selected empirically to describe the observed temperature-time profiles.

Their parameters should not be interpreted as independently validated intrinsic thermal properties of human skin.

## 8. Statistical analysis

Data were analyzed descriptively.

For each specimen and irradiation protocol, the three technical replicates were summarized using mean values and standard deviations.

Exploratory Pearson correlation coefficients were calculated in Microsoft Excel to assess the association between ITA and temperature increase at approximately 30 s of irradiation.

The correlation analysis used specimen-level mean values from five independent biological samples (n = 5).

Technical replicates were not treated as independent biological observations.

Given the limited number of biological specimens, the correlations were interpreted as exploratory.

## 9. Data interpretation and limitations

The experimental results describe surface thermal responses in ex vivo human skin.

The experimental model does not reproduce physiological blood perfusion or thermoregulation.

Differences in tissue thickness, hydration, handling conditions, optical properties, and other specimen characteristics may influence the observed thermal responses.

The temperature measurements were obtained from a single selected surface pixel and should not be interpreted as measurements of internal tissue temperature.

The investigated irradiation protocols differed in optical power and exposure duration. Therefore, differences between individual and simultaneous irradiation should not be interpreted as evidence of wavelength synergy.

The results should not be directly extrapolated to in vivo conditions or used to establish clinical thermal safety thresholds.

## 10. Ethical considerations

The study was approved by the Research Ethics Committee of Ribeirão Preto Medical School, University of São Paulo.

- CAAE: 0630218.2.0000.5440.
- Approval number: 3.275.034.

Written informed consent was obtained from participants before surgery and specimen collection.

Public sharing of experimental data must comply with applicable ethical approvals, consent conditions, and institutional requirements.

Only appropriately de-identified data authorized for sharing should be made publicly available.

## 11. Associated manuscript

**Title:** Surface Heating and Cooling in Ex Vivo Human Skin under 660 nm, 808 nm, and Combined Irradiation: An Exploratory Study of Associations with Skin Color

**Journal:** Lasers in Medical Science

**Status:** Manuscript under revision.
