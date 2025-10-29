# 🏀 Full Court Forecast

**Full Court Forecast** is a college basketball analytics project focused on building a data-driven model to predict NCAA basketball game outcomes. The project leverages large-scale historical data, statistical analysis, and machine learning to explore patterns that influence team performance and game results.

---

## 📘 Project Scope

The goal of this project is to develop an end-to-end machine learning pipeline capable of predicting college basketball outcomes based on advanced statistical features.

### Key Objectives
1. **Data Acquisition & Cleaning**  
   - Scrape multi-season NCAA game logs and team statistics from reliable public sources.  
   - Standardize team names, handle missing values, and ensure consistent data formatting.

2. **Feature Engineering**  
   - Create predictive features from box score and advanced team metrics.  
   - Incorporate contextual variables such as home/away status, recent performance, and opponent strength.

3. **Model Development**  
   - Train and evaluate multiple machine learning models (e.g., Logistic Regression, Random Forest, Gradient Boosting, Neural Networks).  
   - Assess model accuracy, precision, and calibration.

4. **Deployment & Visualization (Future Work)**  
   - Develop a dashboard or API for live game predictions and interactive insights.  
   - Visualize trends and prediction confidence through dashboards or web interfaces.

---

## 🚧 Current Progress

| Phase | Description | Status |
|:------|:-------------|:-------:|
| **Data Scraping** | Collected detailed team and game logs across multiple NCAA seasons | ✅ Completed |
| **Data Cleaning** | Cleaned, merged, and standardized datasets for modeling | ✅ Completed |
| **Feature Engineering** | Constructing advanced team and game-level metrics | ⚙️ In Progress |
| **Machine Learning** | Model selection, training, and evaluation | ⏳ Upcoming |
| **Deployment** | Front-end and visualization tools | 🔜 Planned |

---

## 🧠 Tech Stack

- **Language:** Python  
- **Libraries:** `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `requests`, `beautifulsoup4`  
- **Database:** MySQL (for structured data storage)  
- **Environment:** Jupyter / VS Code  
- **Version Control:** Git + GitHub

---

## 🗂️ Repository Structure

FullCourtForecast/
│
├── .github/workflows/     # GitHub Actions or automation workflows
├── DataFrames/            # Cleaned data and intermediate DataFrames
├── MySQL_Scripts/         # Scripts for database loading and management
├── Prediction/            # Machine learning model training and evaluation
├── Scraping/              # Web scraping scripts and data collection logic
├── .gitignore             # Ignored files and directories
└── README.md              # Project documentation


## 📈 Next Steps

- Engineer predictive variables (recent form, shooting %, opponent rank, etc.)  
- Split datasets into training, validation, and test sets  
- Implement baseline models (Logistic Regression, Random Forest)  
- Compare model performance and iterate on features  
- Visualize predictive accuracy and feature importance  

---

## 📊 Data Sources

- [Sports-Reference: College Basketball](https://www.sports-reference.com/cbb/)   

---

## 🤝 Contributions

Contributions and suggestions are welcome!  
Feel free to open an issue or submit a pull request if you have ideas for improving data quality, adding new models, or optimizing performance.

---

## 🏀 Author

**Logan Becker**   
Computer Science and Data Science Major with a Stats Minor at Iowa State University  
