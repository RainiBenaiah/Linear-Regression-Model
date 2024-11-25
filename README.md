# Smart Irrigation Prediction System for Turkana, Kenya

## Project Resources

### Deployed Application
🔗 Prediction Web App: [https://linear-regression-model-ihov.onrender.com/](https://linear-regression-model-ihov.onrender.com/)

### Demo Video
🎥 Project Demonstration: [OneDrive Video Link](https://1drv.ms/v/c/8f2f111745fa8f97/EXNXH8J5-3FMrvTDuJoeI3MBkWbYherY4MV7SpvPu6ioYw?e=b20QW8)

## Mission Statement

Food insecurity highlights alarming statistics of malnutrition that require urgent attention and comprehensive action all over Africa. Nearly 20% of the African population, around 282 million, are malnourished. Despite the measures taken to address food insecurity, Africa still needs to catch up to meet food security; I step up, promoting nutrition to end all forms of malnutrition.   

My mission focuses on Turkana, Kenya, to combat food insecurity and drought through tailored Smart irrigation solutions, empowering farmers and enhancing community resilience. Through partnerships and pilots, we strive for a 30% agricultural output increase every two years, addressing Turkana farmers' unique challenges.

## Project Description

### Automated Smart Irrigation Prediction System

**Objective:** Develop an intelligent irrigation management solution that predicts soil moisture levels and automatically triggers irrigation when moisture drops below optimal thresholds.

#### Key Features:
- Real-time soil moisture prediction
- Automated irrigation activation
- Precision water resource management
- Drought mitigation for agricultural resilience

**Core Functionality:**
- Continuously monitor environmental parameters
- Predict soil moisture levels
- Automatically initiate irrigation when moisture is low
- Optimize water usage and agricultural productivity

#### Benefits:
- Reduce water waste
- Improve crop yield
- Minimize human intervention in irrigation
- Provide data-driven agricultural support
- Enhance farming efficiency in challenging environmental conditions

## Data Source
Dataset obtained from Kaggle

## Dataset Overview

### Data Characteristics
- Total Entries: 100,000
- Original Columns: 15
- Data Types: 5 integer columns, 10 float columns

### Data Preprocessing

#### Dropped Columns and Rationale
1. **Status**: 
   - Correlation with Soil Moisture: -0.322340 (strongest negative correlation)
   - Likely a categorical or binary indicator that doesn't directly contribute to numerical prediction
   - Might introduce noise or bias in the linear regression model

2. **ph**:
   - Very low correlation with Soil Moisture (close to zero)
   - Limited non-null entries (only 2,200 out of 100,000)
   - Insufficient data for meaningful prediction

3. **N (Nitrogen)**, **P (Phosphorus)**, **K (Potassium)**:
   - Minimal correlation with Soil Moisture
   - Low data completeness (only 2,200 non-null entries)
   - Potential multicollinearity (high correlation among themselves)
     - P and K have a strong correlation of 0.736232
     - Would introduce potential overfitting risks

4. **rainfall**:
   - Weak negative correlation with Soil Moisture (-0.068431)
   - Limited data availability (only 2,200 non-null entries)

## Target Variable
- **Soil Moisture**: Dependent variable for prediction
- Represents the moisture content in the soil

## Independent Variables
Retained variables with their correlations to Soil Moisture:
- Temperature: 0.003622
- Soil Humidity: 0.003141
- Time: -0.001903
- Air temperature (C): -0.005880
- Wind speed (Km/h): -0.010232
- Air humidity (%): 0.005071
- Wind gust (Km/h): -0.009487
- Pressure (KPa): -0.004919

## Model Considerations
- Low correlations suggest a potentially weak linear relationship
- Consider:
  - Feature engineering

## Recommendations
1. Validate model performance carefully
2. Explore alternative modeling approaches
3. Collect more comprehensive data if possible

## Impact Alignment
This automated soil moisture prediction system directly supports the mission of addressing food insecurity in Turkana, Kenya by:
- Providing real-time irrigation insights
- Automating precision water management
- Supporting farmers in managing drought-prone environments
- Contributing to the goal of increasing agricultural output by 30% every two years
- Reducing water waste and improving agricultural efficiency

## Future Development
- Integrate IoT sensors for real-time data collection
- Develop mobile app for farmer monitoring
- Expand to other drought-prone regions in Africa

## Installation and Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Clone the Repository
```bash
git clone https://github.com/your-repository/Linear-Regression-Model.git
cd Linear-Regression-Model
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python main.py
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b ')
3. Commit your changes (`git commit -m ')
4. Push to the branch (`git push origin')
5. Open a Pull Request

## Contact
Your Name - b.raini@alustudent.com

Project Link: [https://linear-regression-model-ihov.onrender.com/](https://linear-regression-model-ihov.onrender.com/)
