# Phishing Website Detection Engine

## High-Level Objective
To analyze and detect malicious (phishing) URLs utilizing a hybrid pipeline combining pre-configured heuristic filtering and advanced Machine Learning (XGBoost) feature extraction.

## Overview
A Python-based framework hosted via a `Streamlit` web application. It ingests raw textual URLs, evaluates their lexical composition through heavily curated rule-based triggers, and routes the structural components to a fast XGBoost tree classifier for a final confidence matrix rating.

---

## 1. Methodology

### 1.1 Data Preparation (`prepare_dataset.py`)
- **Data Integration**: Integrates data from multiple variant sources including `Benign_list_big_final.csv`, `online-valid.csv`, `legitimate.csv`, and `phishing.csv`. 
- **Standardization & Labeling**: Systematically detects the `url` column across wildly different CSV schemas. It applies binary classifications:
  - **Label `0`**: Standard, Benign, Legitimate
  - **Label `1`**: Malicious/Phishing
- **Compilation**: Stacks all records into a single, aggressively shuffled dataframe to eliminate algorithmic bias before exporting to unified `final_url_dataset.csv`.

### 1.2 Feature Extraction Analytics (`utils/feature_extraction.py`)
Utilizes a 16-dimensional lexical vector extraction strategy to dissect raw URLs targeting key adversarial traits:
- **Adversarial Footprints**: Detects raw IP formatting logic (`Have_IP`), credential-stealing `@` routing markers (`Have_At`), excessive `//` injections (`Redirection`), and dash-separated domains designed to closely resemble popular websites (`Prefix/Suffix`).
- **Length & Proportions**: Categorizes URLs by defined length thresholds, evaluates the directory depth footprint (`URL_Depth`), and calculates raw subdomain dots (`.`).
- **Character Topologies**: Extracts hard counts for numerical strings, completely un-worded special characters, query parameters (`?`), and determines SSL validity (`https` schema definitions).

### 1.3 Machine Learning Subsystem (`train_model.py`)
- **Algorithm Strategy**: Deploys `XGBClassifier` (eXtreme Gradient Boosting) optimized on `logloss` criteria. Tree-based learners natively excel at identifying hard threshold parameters like URL segment counts and length dimensions.
- **Optimization Strategy**: Applies an 80/20 training to testing matrix ratio. Serializes the finalized tuned graph representation out to a binary `model.pkl` deployment object via `joblib`.

---

## 2. Real-Time Execution Pipeline 

The framework bridges backend model training and interactive inference through the `app.py` service.

### Phase 1: Interactive Pre-Processing
Captures real-time textual URL links provided directly into the Streamlit portal and standardizes it to uniform lowercase strings.

### Phase 2: Heuristic "Red-Flag" Evaluation (Rule-Based Filter)
The application evaluates the URL across 4 distinct pre-set heuristic tripwires before wasting expensive M.L computation:
1. Short-circuits heavily flagged inputs utilizing raw **IP Addresses** outright (ex. `192.x.x.x`).
2. Isolates inputs containing **`@` Symbols** (commonly deployed to hide actual endpoint IPs).
3. Warns on extreme domain fragmentation (counting extensive subdomains exceeding 4 dot `.` separators).
4. Matches the payload against a localized "sensitive keyword dictionary" (`login`, `verify`, `bank`, `secure`, `update`) utilized actively by threat actors mimicking financial applications.

### Phase 3: Matrix Prediction Execution
If the URL circumvents basic heuristic filters, the `extract_features` generator breaks the text down into its 16-element analytical footprint matrix. It is reshaped, ingested by the serialized XGBoost engine, and processed—returning binary labels joined tightly by an extrapolated algorithmic Confidence Percentage UI layer.

---

## 3. Setup & Operational Instructions

### 3.1 Dependencies
Require base analytical and UI libraries installed inside your environment:
```bash
pip install pandas numpy xgboost scikit-learn joblib streamlit
```

### 3.2 Pipeline Execution Protocol

**1. Bootstrap the Dataset Pipeline**
Generate the unified raw CSV files required by the classifier backend payload:
```bash
python prepare_dataset.py
```

**2. Retrain the Classification Engine**
Launch feature extraction sequences against the compiled dataset to map the updated XGBoost classifier logic:
```bash
python train_model.py
```

**3. Initialize Interface**
Stand up the continuous local web application engine utilizing the compiled weights (`model.pkl`):
```bash
streamlit run app.py
```
