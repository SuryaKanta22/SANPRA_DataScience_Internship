import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_full_analysis():
    try:
        # Set output directory
        OUTPUT_DIR = 'Output/'
        
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        # Load Data
        df = pd.read_csv('Global_Superstore2.csv', encoding='latin1')
        
        # Data Cleaning
        # Drop Postal Code (too many missing values)
        df.drop(columns=['Postal Code'], inplace=True)
        
        # Convert Dates
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
        
        # Extract Month-Year for trend analysis
        df['Month-Year'] = df['Order Date'].dt.to_period('M')

        # Set style
        sns.set(style="whitegrid")
        
        # 1. Sales Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Sales'], bins=50, kde=True, color='blue')
        plt.title('Distribution of Sales')
        plt.xlabel('Sales')
        plt.ylabel('Frequency')
        plt.savefig(OUTPUT_DIR + '1_sales_distribution.png')
        plt.close()
        
        # 2. Sales vs Profit (Scatter Plot)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Sales', y='Profit', data=df, hue='Category', alpha=0.6)
        plt.title('Sales vs Profit by Category')
        plt.savefig(OUTPUT_DIR + '2_sales_vs_profit.png')
        plt.close()
        
        # 3. Sales by Category (Bar Chart)
        category_sales = df.groupby('Category')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False)
        plt.figure(figsize=(8, 5))
        sns.barplot(x='Category', y='Sales', data=category_sales, palette='viridis')
        plt.title('Total Sales by Category')
        plt.savefig(OUTPUT_DIR + '3_sales_by_category.png')
        plt.close()
        
        # 4. Monthly Sales Trend (Line Chart)
        monthly_sales = df.groupby('Month-Year')['Sales'].sum()
        monthly_sales.index = monthly_sales.index.astype(str)
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_sales.index, monthly_sales.values, marker='o', linestyle='-')
        plt.title('Monthly Sales Trend')
        plt.xticks(rotation=45)
        plt.xlabel('Month-Year')
        plt.ylabel('Total Sales')
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR + '4_monthly_sales_trend.png')
        plt.close()
        
        # 5. Profit by Region (Bar Chart)
        region_profit = df.groupby('Region')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False)
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Profit', y='Region', data=region_profit, palette='magma')
        plt.title('Total Profit by Region')
        plt.xlabel('Total Profit')
        plt.ylabel('Region')
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR + '5_profit_by_region.png')
        plt.close()

        # 6. Correlation Heatmap
        plt.figure(figsize=(8, 6))
        numeric_df = df[['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Cost']]
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Heatmap')
        plt.savefig(OUTPUT_DIR + '6_correlation_heatmap.png')
        plt.close()

        # Generate Report
        with open(OUTPUT_DIR + 'final_report.md', 'w') as f:
            f.write("# Global Superstore Sales Analysis Report\n\n")
            f.write("## Data Overview\n")
            f.write(f"- **Total Records**: {len(df)}\n")
            f.write(f"- **Total Sales**: ${df['Sales'].sum():,.2f}\n")
            f.write(f"- **Total Profit**: ${df['Profit'].sum():,.2f}\n\n")
            
            f.write("## Key Insights\n")
            f.write("1. **Sales Distribution**: The sales distribution is highly right-skewed, indicating most transactions are of low value, with a few high-value outliers.\n")
            f.write("2. **Sales vs Profit**: There is a positive correlation, but high sales do not always guarantee high profit, likely due to discounts.\n")
            f.write(f"3. **Top Category**: {category_sales.iloc[0]['Category']} generates the highest sales.\n")
            f.write(f"4. **Most Profitable Region**: {region_profit.iloc[0]['Region']} is the most profitable region.\n")
            f.write("5. **Seasonality**: Monthly sales show trends and seasonality (refer to trend chart).\n\n")
            
            f.write("## Visualizations\n")
            f.write("![Sales Distribution](1_sales_distribution.png)\n")
            f.write("![Sales vs Profit](2_sales_vs_profit.png)\n")
            f.write("![Sales by Category](3_sales_by_category.png)\n")
            f.write("![Monthly Sales Trend](4_monthly_sales_trend.png)\n")
            f.write("![Profit by Region](5_profit_by_region.png)\n")
            f.write("![Correlation Heatmap](6_correlation_heatmap.png)\n")

        print("\nAnalysis complete. \nReport and visualizations generated.\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_full_analysis()
