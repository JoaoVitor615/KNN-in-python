"""
Data Loader Module
Loads and validates sales data from Excel files.
Only 'date' and 'sales' fields are required.
Other fields are automatically detected as customizable features.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class SalesDataLoader:
    """
    Class responsible for loading and validating sales data from Excel files.
    """
    
    def __init__(self):
        self.required_columns = ['date', 'sales']
        self.data = None
        self.custom_columns = []
        
    def load_excel(self, file_path: str) -> pd.DataFrame:
        """
        Loads data from Excel file and validates required fields.
        
        Args:
            file_path (str): Path to the Excel file
            
        Returns:
            pd.DataFrame: DataFrame with loaded data
            
        Raises:
            FileNotFoundError: If file is not found
            ValueError: If required fields are missing
        """
        try:
            # Load Excel file
            print(f"📂 Loading file: {file_path}")
            self.data = pd.read_excel(file_path)
            
            # Validate required columns
            self._validate_required_columns()
            
            # Process date column
            self._process_date_column()
            
            # Detect custom features
            self._detect_custom_columns()
            
            # Show basic information
            self._show_data_info()
            
            return self.data
            
        except FileNotFoundError:
            raise FileNotFoundError(f"❌ File not found: {file_path}")
        except Exception as e:
            raise Exception(f"❌ Error loading file: {str(e)}")
    
    def _validate_required_columns(self):
        """Validates if required fields are present."""
        missing_columns = []
        
        for col in self.required_columns:
            if col not in self.data.columns:
                missing_columns.append(col)
        
        if missing_columns:
            raise ValueError(f"❌ Required fields missing: {missing_columns}")
        
        print("✅ Required fields validated successfully!")
    
    
    def _process_date_column(self):
        """Processes and validates the date column."""
        try:
            # Convert to datetime if not already
            if not pd.api.types.is_datetime64_any_dtype(self.data['date']):
                self.data['date'] = pd.to_datetime(self.data['date'])
            
            # Check for invalid dates
            if self.data['date'].isnull().any():
                null_count = self.data['date'].isnull().sum()
                print(f"⚠️  Found {null_count} invalid dates")
            
            print("✅ Date column processed successfully!")
            
        except Exception as e:
            raise ValueError(f"❌ Error processing date column: {str(e)}")
    
    def _detect_custom_columns(self):
        """Automatically detects customizable features."""
        # All columns except required ones are customizable features
        self.custom_columns = [col for col in self.data.columns 
                               if col not in self.required_columns]
        
        if self.custom_columns:
            print(f"🎯 Custom features detected: {self.custom_columns}")
        else:
            print("ℹ️  No custom features found (basic data only)")
    
    def _show_data_info(self):
        """Shows basic information about loaded data."""
        print("\n" + "="*50)
        print("📊 LOADED DATA INFORMATION")
        print("="*50)
        
        print(f"📅 Period: {self.data['date'].min().strftime('%d/%m/%Y')} to {self.data['date'].max().strftime('%d/%m/%Y')}")
        print(f"📈 Total records: {len(self.data)}")
        print(f"💰 Average sales: $ {self.data['sales'].mean():.2f}")
        print(f"💰 Minimum sales: $ {self.data['sales'].min():.2f}")
        print(f"💰 Maximum sales: $ {self.data['sales'].max():.2f}")
        
        if self.custom_columns:
            print(f"\n🎯 Custom features ({len(self.custom_columns)}):")
            for feature in self.custom_columns:
                feature_type = self.data[feature].dtype
                print(f"  • {feature}: {feature_type}")
        
        print("\n📋 First 3 rows:")
        print(self.data.head(3).to_string(index=False))
        print("="*50)
    
        """
        Returns a summary of loaded data.
        
        Returns:
            Dict: Dictionary with summarized information
        """
        if self.data is None:
            return {"error": "No data loaded"}
        
        return {
            "total_records": len(self.data),
            "date_range": {
                "start": self.data['date'].min().strftime('%Y-%m-%d'),
                "end": self.data['date'].max().strftime('%Y-%m-%d')
            },
            "sales_stats": {
                "mean": float(self.data['sales'].mean()),
                "min": float(self.data['sales'].min()),
                "max": float(self.data['sales'].max()),
                "std": float(self.data['sales'].std())
            },
            "custom_columns": self.custom_columns,
            "missing_values": self.data.isnull().sum().to_dict()
        }


# Convenience function for quick usage
def load_sales_data(file_path: str) -> Tuple[pd.DataFrame, SalesDataLoader]:
    """
    Convenience function to load sales data.
    
    Args:
        file_path (str): Path to the Excel file
        
    Returns:
        Tuple[pd.DataFrame, SalesDataLoader]: Loaded data and loader instance
    """
    loader = SalesDataLoader()
    data = loader.load_excel(file_path)
    return data, loader