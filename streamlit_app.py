import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Student Marks Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #0066ff;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/student_marks.csv')
    return df

# Title and description
st.title("📊 Student Marks Analysis Dashboard")
st.markdown("A comprehensive analysis of student academic performance across multiple subjects")

# Load the dataset
try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ Error: Could not find 'data/student_marks.csv'. Please ensure the file exists in the data folder.")
    st.stop()

# Define subjects
subjects = ['Mathematics', 'Physics', 'Chemistry', 'English', 'History']

# Calculate derived columns
df['Total_Marks'] = df[subjects].sum(axis=1)
df['Average_Marks'] = df[subjects].mean(axis=1)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a section:",
    [
        "📈 Overview",
        "📋 Data Explorer",
        "📊 Subject Statistics",
        "👥 Student Performance",
        "📉 Visualizations",
        "🎯 Summary & Insights"
    ]
)

# ============================================================================
# PAGE 1: OVERVIEW
# ============================================================================
if page == "📈 Overview":
    st.header("Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Students",
            value=len(df),
            delta="15 records"
        )
    
    with col2:
        st.metric(
            label="Total Subjects",
            value=len(subjects),
            delta="5 courses"
        )
    
    with col3:
        st.metric(
            label="Avg Class Score",
            value=f"{df[subjects].values.mean():.2f}",
            delta=f"out of 100"
        )
    
    with col4:
        st.metric(
            label="Highest Score",
            value=int(df[subjects].values.max()),
            delta=f"marks"
        )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
    
    with col2:
        st.subheader("Dataset Info")
        st.info(f"""
        **Dataset Shape:** {df.shape[0]} rows × {df.shape[1]} columns
        
        **Columns:**
        - Student ID & Name
        - 5 Subjects: {', '.join(subjects)}
        - Calculated: Total & Average Marks
        
        **Data Type:** CSV
        """)

# ============================================================================
# PAGE 2: DATA EXPLORER
# ============================================================================
elif page == "📋 Data Explorer":
    st.header("Data Explorer")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Full Dataset")
    
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Student ID", "Name", "Average_Marks", "Total_Marks"],
            key="sort_select"
        )
    
    # Sort dataframe
    if sort_by == "Average_Marks":
        display_df = df.sort_values("Average_Marks", ascending=False)
    elif sort_by == "Total_Marks":
        display_df = df.sort_values("Total_Marks", ascending=False)
    else:
        display_df = df.sort_values(sort_by)
    
    # Display with formatting
    display_cols = ['Student_ID', 'Name'] + subjects + ['Total_Marks', 'Average_Marks']
    st.dataframe(
        display_df[display_cols].assign(**{col: display_df[col].apply(lambda x: f"{x:.1f}" if isinstance(x, float) else x) 
                                           for col in ['Average_Marks']}),
        use_container_width=True
    )
    
    st.divider()
    
    # Search functionality
    st.subheader("Search Student")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_student = st.text_input("Enter student name (partial match):", "")
    
    if search_student:
        filtered_df = df[df['Name'].str.contains(search_student, case=False, na=False)]
        if len(filtered_df) > 0:
            st.success(f"Found {len(filtered_df)} student(s)")
            st.dataframe(filtered_df[display_cols], use_container_width=True)
        else:
            st.warning("No students found matching that name")

# ============================================================================
# PAGE 3: SUBJECT STATISTICS
# ============================================================================
elif page == "📊 Subject Statistics":
    st.header("Subject-wise Statistics")
    
    # Calculate statistics
    stats_data = {
        'Subject': subjects,
        'Average': [df[subject].mean() for subject in subjects],
        'Maximum': [df[subject].max() for subject in subjects],
        'Minimum': [df[subject].min() for subject in subjects],
        'Std Dev': [df[subject].std() for subject in subjects]
    }
    stats_df = pd.DataFrame(stats_data)
    
    st.subheader("Statistical Summary Table")
    st.dataframe(
        stats_df.style.format({
            'Average': '{:.2f}',
            'Std Dev': '{:.2f}'
        }).background_gradient(subset=['Average'], cmap='viridis'),
        use_container_width=True
    )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Best & Worst Subjects")
        best_subject = stats_df.loc[stats_df['Average'].idxmax()]
        worst_subject = stats_df.loc[stats_df['Average'].idxmin()]
        
        col_best, col_worst = st.columns(2)
        with col_best:
            st.success(f"""
            **Best Performing Subject**
            
            📚 {best_subject['Subject']}
            
            Avg: {best_subject['Average']:.2f}
            """)
        
        with col_worst:
            st.info(f"""
            **Lowest Performing Subject**
            
            📚 {worst_subject['Subject']}
            
            Avg: {worst_subject['Average']:.2f}
            """)
    
    with col2:
        st.subheader("Subject Difficulty")
        st.caption("Lower variability = More consistent performance")
        
        variability_data = {
            'Subject': subjects,
            'Variability (IQR)': [df[subject].quantile(0.75) - df[subject].quantile(0.25) for subject in subjects]
        }
        var_df = pd.DataFrame(variability_data).sort_values('Variability (IQR)', ascending=True)
        
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#FF6B6B' if x > var_df['Variability (IQR)'].mean() else '#4ECDC4' 
                  for x in var_df['Variability (IQR)']]
        ax.barh(var_df['Subject'], var_df['Variability (IQR)'], color=colors, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Variability (IQR)', fontweight='bold')
        ax.set_title('Subject Difficulty Index', fontweight='bold', fontsize=12)
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig, use_container_width=True)

# ============================================================================
# PAGE 4: STUDENT PERFORMANCE
# ============================================================================
elif page == "👥 Student Performance":
    st.header("Student Performance Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Student Rankings")
    
    with col2:
        top_n = st.number_input("Show top N students:", min_value=1, max_value=15, value=5)
    
    # Top performers
    top_students = df.nlargest(top_n, 'Average_Marks')[['Student_ID', 'Name', 'Total_Marks', 'Average_Marks']]
    
    for idx, (i, row) in enumerate(top_students.iterrows(), 1):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.metric(f"#{idx}", row['Name'], f"{row['Average_Marks']:.1f}")
        with col2:
            st.progress(row['Average_Marks'] / 100, text=f"Total: {int(row['Total_Marks'])}/500")
    
    st.divider()
    
    # Performance categories
    st.subheader("Performance Distribution")
    
    excellent = (df['Average_Marks'] >= 85).sum()
    good = ((df['Average_Marks'] >= 75) & (df['Average_Marks'] < 85)).sum()
    average = ((df['Average_Marks'] >= 65) & (df['Average_Marks'] < 75)).sum()
    below = (df['Average_Marks'] < 65).sum()
    
    perf_data = {
        'Category': ['Excellent (≥85)', 'Good (75-84)', 'Average (65-74)', 'Below Average (<65)'],
        'Count': [excellent, good, average, below],
        'Percentage': [
            excellent/len(df)*100,
            good/len(df)*100,
            average/len(df)*100,
            below/len(df)*100
        ]
    }
    perf_df = pd.DataFrame(perf_data)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_perf = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
        wedges, texts, autotexts = ax.pie(perf_df['Count'], labels=perf_df['Category'], autopct='%1.1f%%',
                                           colors=colors_perf, startangle=90, textprops={'fontsize': 10})
        ax.set_title('Student Performance Distribution', fontweight='bold', fontsize=12)
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        st.dataframe(perf_df, use_container_width=True, hide_index=True)

# ============================================================================
# PAGE 5: VISUALIZATIONS
# ============================================================================
elif page == "📉 Visualizations":
    st.header("Data Visualizations")
    
    viz_type = st.selectbox(
        "Select visualization:",
        [
            "Average Marks by Subject",
            "Max & Min Marks by Subject",
            "Student Performance Comparison",
            "Total Marks Distribution",
            "Subject Comparison (Top Students)",
            "Heatmap of Subject Performance"
        ]
    )
    
    if viz_type == "Average Marks by Subject":
        fig, ax = plt.subplots(figsize=(10, 5))
        averages = [df[subject].mean() for subject in subjects]
        colors_avg = plt.cm.viridis(np.linspace(0.3, 0.9, len(subjects)))
        bars = ax.bar(subjects, averages, color=colors_avg, edgecolor='black', linewidth=1.5, alpha=0.8)
        ax.set_ylabel('Average Marks', fontweight='bold', fontsize=11)
        ax.set_title('Average Marks Per Subject', fontweight='bold', fontsize=13)
        ax.set_ylim(0, 100)
        ax.grid(axis='y', alpha=0.3)
        for i, v in enumerate(averages):
            ax.text(i, v + 1, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig, use_container_width=True)
    
    elif viz_type == "Max & Min Marks by Subject":
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        maximums = [df[subject].max() for subject in subjects]
        minimums = [df[subject].min() for subject in subjects]
        
        ax1.bar(subjects, maximums, color='#2ecc71', edgecolor='darkgreen', linewidth=1.5, alpha=0.8)
        ax1.set_ylabel('Maximum Marks', fontweight='bold')
        ax1.set_title('Maximum Marks Per Subject', fontweight='bold')
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y', alpha=0.3)
        for i, v in enumerate(maximums):
            ax1.text(i, v + 1, f'{v}', ha='center', va='bottom', fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        
        ax2.bar(subjects, minimums, color='#e74c3c', edgecolor='darkred', linewidth=1.5, alpha=0.8)
        ax2.set_ylabel('Minimum Marks', fontweight='bold')
        ax2.set_title('Minimum Marks Per Subject', fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.grid(axis='y', alpha=0.3)
        for i, v in enumerate(minimums):
            ax2.text(i, v + 1, f'{v}', ha='center', va='bottom', fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
    
    elif viz_type == "Student Performance Comparison":
        fig, ax = plt.subplots(figsize=(12, 6))
        sorted_df = df.sort_values('Average_Marks', ascending=False)
        colors_gradient = plt.cm.viridis(np.linspace(0.3, 0.9, len(sorted_df)))
        ax.barh(sorted_df['Name'], sorted_df['Average_Marks'], color=colors_gradient, edgecolor='black', linewidth=0.5)
        ax.set_xlabel('Average Marks', fontweight='bold')
        ax.set_title('Student Performance Ranking', fontweight='bold', fontsize=13)
        ax.set_xlim(0, 100)
        ax.grid(axis='x', alpha=0.3)
        for i, v in enumerate(sorted_df['Average_Marks']):
            ax.text(v + 1, i, f'{v:.1f}', va='center', fontweight='bold', fontsize=9)
        st.pyplot(fig, use_container_width=True)
    
    elif viz_type == "Total Marks Distribution":
        fig, ax = plt.subplots(figsize=(12, 6))
        sorted_df = df.sort_values('Total_Marks', ascending=False)
        colors_gradient = plt.cm.plasma(np.linspace(0.3, 0.9, len(sorted_df)))
        bars = ax.bar(range(len(sorted_df)), sorted_df['Total_Marks'], color=colors_gradient, edgecolor='black', linewidth=0.5)
        ax.set_xlabel('Students', fontweight='bold')
        ax.set_ylabel('Total Marks (out of 500)', fontweight='bold')
        ax.set_title('Total Marks Comparison', fontweight='bold', fontsize=13)
        ax.set_xticks(range(len(sorted_df)))
        ax.set_xticklabels(sorted_df['Name'], rotation=45, ha='right')
        ax.set_ylim(0, 500)
        ax.grid(axis='y', alpha=0.3)
        for i, v in enumerate(sorted_df['Total_Marks']):
            ax.text(i, v + 5, f'{int(v)}', ha='center', va='bottom', fontweight='bold', fontsize=8)
        st.pyplot(fig, use_container_width=True)
    
    elif viz_type == "Subject Comparison (Top Students)":
        top_n_sub = st.slider("Number of top students:", 3, 10, 5)
        top_5_students = df.nlargest(top_n_sub, 'Average_Marks')
        
        fig, ax = plt.subplots(figsize=(12, 6))
        x_pos = np.arange(len(subjects))
        width = 0.15
        colors = plt.cm.Set3(np.linspace(0, 1, top_n_sub))
        
        for idx, (_, student_row) in enumerate(top_5_students.iterrows()):
            marks = [student_row[subject] for subject in subjects]
            ax.bar(x_pos + (idx * width), marks, width, label=student_row['Name'], color=colors[idx], alpha=0.8)
        
        ax.set_xlabel('Subjects', fontweight='bold')
        ax.set_ylabel('Marks', fontweight='bold')
        ax.set_title(f'Top {top_n_sub} Students - Subject Comparison', fontweight='bold', fontsize=13)
        ax.set_xticks(x_pos + width * (top_n_sub - 1) / 2)
        ax.set_xticklabels(subjects)
        ax.legend(loc='upper left', framealpha=0.9, fontsize=9)
        ax.set_ylim(0, 100)
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig, use_container_width=True)
    
    elif viz_type == "Heatmap of Subject Performance":
        # Prepare data for heatmap
        heatmap_data = df[['Name'] + subjects].set_index('Name')
        
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(heatmap_data.values, cmap='RdYlGn', aspect='auto', vmin=60, vmax=100)
        
        ax.set_xticks(np.arange(len(subjects)))
        ax.set_yticks(np.arange(len(heatmap_data)))
        ax.set_xticklabels(subjects, rotation=45, ha='right')
        ax.set_yticklabels(heatmap_data.index, fontsize=9)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Marks', rotation=270, labelpad=15, fontweight='bold')
        
        # Add text annotations
        for i in range(len(heatmap_data)):
            for j in range(len(subjects)):
                text = ax.text(j, i, int(heatmap_data.values[i, j]),
                             ha="center", va="center", color="black", fontsize=8, fontweight='bold')
        
        ax.set_title('Student Performance Heatmap', fontweight='bold', fontsize=13, pad=20)
        st.pyplot(fig, use_container_width=True)

# ============================================================================
# PAGE 6: SUMMARY & INSIGHTS
# ============================================================================
elif page == "🎯 Summary & Insights":
    st.header("Summary & Key Insights")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        best_subject = stats_df.loc[stats_df['Average'].idxmax()]
        st.metric("🏆 Best Subject", best_subject['Subject'], f"{best_subject['Average']:.1f}")
    
    with col2:
        worst_subject = stats_df.loc[stats_df['Average'].idxmin()]
        st.metric("📉 Lowest Subject", worst_subject['Subject'], f"{worst_subject['Average']:.1f}")
    
    with col3:
        top_student = df.loc[df['Average_Marks'].idxmax()]
        st.metric("👑 Top Performer", top_student['Name'], f"{top_student['Average_Marks']:.1f}")
    
    with col4:
        bottom_student = df.loc[df['Average_Marks'].idxmin()]
        st.metric("📚 Room to Improve", bottom_student['Name'], f"{bottom_student['Average_Marks']:.1f}")
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Key Findings")
        
        class_avg = df[subjects].values.mean()
        highest_score = df[subjects].values.max()
        lowest_score = df[subjects].values.min()
        
        st.markdown(f"""
        - **Class Average**: {class_avg:.2f} marks
        - **Highest Score**: {int(highest_score)} marks
        - **Lowest Score**: {int(lowest_score)} marks
        - **Score Range**: {int(highest_score - lowest_score)} marks
        - **Total Students**: {len(df)}
        - **Average Class Performance**: {df['Average_Marks'].mean():.2f}%
        """)
    
    with col2:
        st.subheader("📈 Performance Insights")
        
        excellent_count = (df['Average_Marks'] >= 85).sum()
        good_count = ((df['Average_Marks'] >= 75) & (df['Average_Marks'] < 85)).sum()
        avg_count = ((df['Average_Marks'] >= 65) & (df['Average_Marks'] < 75)).sum()
        below_count = (df['Average_Marks'] < 65).sum()
        
        st.markdown(f"""
        **Student Distribution:**
        - 🌟 Excellent (≥85): {excellent_count} ({excellent_count/len(df)*100:.1f}%)
        - ✅ Good (75-84): {good_count} ({good_count/len(df)*100:.1f}%)
        - 📖 Average (65-74): {avg_count} ({avg_count/len(df)*100:.1f}%)
        - ⚠️ Below Avg (<65): {below_count} ({below_count/len(df)*100:.1f}%)
        """)
    
    st.divider()
    
    st.subheader("📋 Subject Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success(f"""
        **✨ Strength Area**
        
        Students excel in:
        **{best_subject['Subject']}**
        
        Avg: {best_subject['Average']:.2f}
        """)
    
    with col2:
        st.warning(f"""
        **⚠️ Focus Area**
        
        Needs improvement:
        **{worst_subject['Subject']}**
        
        Avg: {worst_subject['Average']:.2f}
        """)
    
    with col3:
        improvement_potential = best_subject['Average'] - worst_subject['Average']
        st.info(f"""
        **🚀 Growth Potential**
        
        Improvement gap:
        **{improvement_potential:.2f}** marks
        """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
    <p>📚 Student Marks Analysis Dashboard | Data Science Project | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
