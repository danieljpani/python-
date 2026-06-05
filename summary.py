import sys
import json
import pandas as pd

def load_data(filepath):
    # TODO: load the CSV and return a DataFrame
    df = pd.read_csv(filepath)
    return df

def summarise_numeric(series):
    # TODO: return dict with min, max, mean, median, std
    return {
        'min': float(series.min()),
        'max': float(series.max()),
        'mean': float(series.mean()),
        'median': float(series.median()),
        'std': float(series.std())
    }

def summarise_text(series):
    # TODO: return dict with unique count and most common value
    most_common = series.mode()
    
    return {
        'unique_count': int(series.nunique()),
        # .mode() returns a series because there can be a tie. 
        # We grab index 0 to get the first most common value.
        'most_common': most_common.iloc[0] if not most_common.empty else None
    }

def generate_report(df):
    report = {
        'shape': {'rows': df.shape[0], 'cols': df.shape[1]},
        'columns': {}
    }
    for col in df.columns:
        series = df[col]
        
        # 1. Count missing values for this column
        missing_count = int(series.isna().sum())
        
        # 2. Check the data type of the column
        # If it's numeric (integers or floats)
        if pd.api.types.is_numeric_dtype(series):
            stats = summarise_numeric(series)
        # If it's text/object data
        else:
            stats = summarise_text(series)
            
        # 3. Add the missing values count into our stats dictionary
        stats['missing_values'] = missing_count
        
        # 4. Save this column's report into the main report dictionary
        report['columns'][col] = stats
        
    return report

def main():
    if len(sys.argv) < 2:
        print('Usage: python summary.py <filename.csv>')
        sys.exit(1)
        
    filepath = sys.argv[1]
    df = load_data(filepath)
    report = generate_report(df)
    
    # 🌟 Push these lines inside the function (Add a tab/4 spaces):
    print("\n📊 --- DATA SUMMARY REPORT --- 📊")
    print(json.dumps(report, indent=4))
    
    with open('summary.json', 'w') as f:
        json.dump(report, f, indent=4)
    print("\n💾 Report successfully saved to 'summary.json'!")

if __name__ == '__main__':
    main()