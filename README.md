# Student Marks Analysis - Data Science College Project

A comprehensive data science project analyzing student academic performance across multiple subjects using Python, pandas, and matplotlib.

## 📋 Project Overview

This project teaches fundamental data science concepts through real-world academic data analysis:

### What Students Learn:
- **Data Import**: Reading CSV files using `pd.read_csv()`
- **Data Manipulation**: Column operations and aggregations
- **Statistical Analysis**: Calculating mean(), max(), and min() for different groups
- **Data Visualization**: Creating bar charts to compare and analyze data
- **Data Insights**: Drawing meaningful conclusions from visualizations

## 📊 Concepts Tested

✓ `pd.read_csv()` - Load data from CSV files  
✓ Column operations - Arithmetic and logical operations on columns  
✓ `mean()`, `max()`, `min()` - Statistical aggregation functions  
✓ `plt.bar()` - Basic bar plot visualization  
✓ Data sorting and grouping operations  
✓ Pandas DataFrame manipulation

## 📁 Project Structure

```
├── README.md
├── student_marks_analysis.ipynb
└── data/
    └── student_marks.csv
```

## 📚 Dataset

**File**: `data/student_marks.csv`

**Contents**: 15 students with marks in 5 subjects:
- Student ID
- Name
- Mathematics
- Physics
- Chemistry
- English
- History

**Marks Range**: 0-100 per subject

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas matplotlib jupyter numpy
```

### Execute
```bash
cd /workspaces/minor-project-2
jupyter notebook student_marks_analysis.ipynb
```

Then run all cells to see the complete analysis.

## 📈 Analysis Sections

1. **Load Dataset** - Import and explore data structure
2. **Data Exploration** - Check data types, missing values, and summary statistics
3. **Statistical Calculations** - Compute mean, max, min per subject
4. **Student Performance** - Calculate total and average marks per student
5. **Subject Visualization** - Compare average, max, min marks across subjects
6. **Student Comparison** - Bar charts comparing top 5 students
7. **Total Marks Comparison** - All students ranked by total performance
8. **Subject Analysis** - Variability and distribution analysis
9. **Summary Report** - Key insights and performance distribution

## 🎯 Key Outputs

- Subject-wise average, maximum, and minimum marks
- Student rankings by performance
- Top and bottom performers identification
- Performance distribution categories (Excellent, Good, Average, Below Average)
- Visual comparisons through multiple bar charts

## 📝 Learning Outcomes

After completing this project, students will be able to:
1. Load and explore CSV data using pandas
2. Perform basic statistical analysis on datasets
3. Create professional visualizations with matplotlib
4. Compare and contrast data using multiple dimensions
5. Draw meaningful insights from data analysis
6. Present data analysis results clearly through charts

## 💡 Extensions (Optional)

- Add more subjects to the dataset
- Calculate percentile rankings
- Create pie charts for grade distribution
- Add CSV export of analysis results
- Implement data filtering and advanced queries
- Create a summary report document

## 🔗 Data Source

This project uses a custom student marks dataset created for educational purposes. Students can modify the `data/student_marks.csv` file to include their own school or college data, or find similar datasets on:
- [Kaggle - Student Performance Datasets](https://www.kaggle.com/search?q=student+marks)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)

## 🌐 Streamlit Deployment

### Run Streamlit App Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

### Features in Streamlit Dashboard

- **📈 Overview** - Quick statistics and data preview
- **📋 Data Explorer** - Browse and search student data
- **📊 Subject Statistics** - Detailed subject-wise analysis
- **👥 Student Performance** - Ranking and distribution charts
- **📉 Visualizations** - Interactive charts and heatmaps
- **🎯 Summary & Insights** - Key findings and recommendations

### Deploy to Cloud

#### Option 1: Deploy on Streamlit Cloud (Free)
1. Push your repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" and select your GitHub repository
4. Set main file path to `streamlit_app.py`
5. Click "Deploy"

#### Option 2: Deploy on Heroku
```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py" > Procfile

# Push to Heroku
git push heroku main
```

#### Option 3: Deploy on AWS, Google Cloud, Azure
Follow their respective containerization guidelines with the provided `requirements.txt`

## 📞 Notes

- All marks are out of 100 per subject
- Calculations use built-in pandas statistical functions
- Charts include value labels for clarity
- Code includes explanatory comments for learning
- Streamlit app provides interactive data exploration and visualization