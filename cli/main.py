"""
KNN Sales Prediction - Command Line Interface
Main entry point for the terminal-based sales prediction system.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional

# Add src directory to path to import our modules
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_loader import SalesDataLoader


class SalesPredictionCLI:
    """
    Command Line Interface for the KNN Sales Prediction System.
    """
    
    def __init__(self):
        self.data_loader = SalesDataLoader()
        self.input_dir = Path(__file__).parent.parent / 'data' / 'input'
        self.current_data = None
        
    def run(self):
        """Main CLI loop."""
        print("\n🎯 KNN Sales Prediction System")
        
        while True:
            try:
                # Show main menu
                self._show_main_menu()
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '1':
                    self._select_and_load_file()
                elif choice == '2':
                    self._show_data_info()
                elif choice == '3':
                    self._make_prediction()
                elif choice == '0':
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
            input("\nPress Enter to continue...")
    
    def _show_main_menu(self):
        """Display the main menu options."""
        print("\n" + "=" * 40)
        print("📋 MAIN MENU")
        print("=" * 40)
        print("1. 📂 Select and load data file")
        print("2. 📊 Show current data information")
        print("3. 🔮 Make sales prediction")
        print("0. 🚪 Exit")
        
        if self.current_data is not None:
            print(f"\n✅ Current file loaded: {len(self.current_data)} records")
        else:
            print("\n⚠️  No file loaded yet")
    
    def _select_and_load_file(self):
        """List available files and let user select one."""
        print("\n" + "=" * 40)
        print("📂 SELECT DATA FILE")
        print("=" * 40)
        
        # Get list of Excel files in input directory
        excel_files = self._get_excel_files()
        
        if not excel_files:
            print("❌ No Excel files found in data/input directory.")
            print("Please add your Excel files to the data/input folder.")
            return
        
        # Display available files
        print("Available files:")
        for i, file_name in enumerate(excel_files, 1):
            file_path = self.input_dir / file_name
            try:
                # Get file size
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"{i}. {file_name} ({size_mb:.2f} MB)")
            except:
                print(f"{i}. {file_name}")
        
        print("0. Cancel")
        
        # Get user selection
        try:
            choice = int(input(f"\nSelect file (1-{len(excel_files)}): ").strip())
            
            if choice == 0:
                return
            elif 1 <= choice <= len(excel_files):
                selected_file = excel_files[choice - 1]
                file_path = self.input_dir / selected_file
                
                # Load the selected file
                print(f"\n🔄 Loading {selected_file}...")
                self.current_data = self.data_loader.load_excel(str(file_path))
                print(f"✅ File loaded successfully!")
                
            else:
                print("❌ Invalid selection.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error loading file: {e}")
    
    def _get_excel_files(self) -> List[str]:
        """Get list of Excel files in the input directory."""
        if not self.input_dir.exists():
            return []
        
        excel_extensions = ['.xlsx', '.xls']
        excel_files = []
        
        for file_path in self.input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in excel_extensions:
                excel_files.append(file_path.name)
        
        return sorted(excel_files)
    
    def _show_data_info(self):
        """Show information about currently loaded data."""
        if self.current_data is None:
            print("\n❌ No data loaded. Please select a file first.")
            return
        
        print("\n" + "=" * 40)
        print("📊 CURRENT DATA INFORMATION")
        print("=" * 40)
        
        # The data_loader already shows detailed info when loading
        # Here we can show a summary
        print(f"📈 Total records: {len(self.current_data)}")
        print(f"📅 Date range: {self.current_data['date'].min().strftime('%d/%m/%Y')} to {self.current_data['date'].max().strftime('%d/%m/%Y')}")
        print(f"💰 Sales range: ${self.current_data['sales'].min():.2f} - ${self.current_data['sales'].max():.2f}")
        
        if self.data_loader.custom_columns:
            print(f"🎯 Custom features: {', '.join(self.data_loader.custom_columns)}")
        
        # Show sample data
        print("\n📋 Sample data:")
        print(self.current_data.head(3).to_string(index=False))
    
    def _make_prediction(self):
        """Make sales prediction (placeholder for now)."""
        if self.current_data is None:
            print("\n❌ No data loaded. Please select a file first.")
            return
        
        print("\n" + "=" * 40)
        print("🔮 SALES PREDICTION")
        print("=" * 40)
        print("🚧 Prediction functionality will be implemented in the next step!")
        print("📊 Current data is ready for KNN model training.")


def main():
    """Entry point for the CLI application."""
    cli = SalesPredictionCLI()
    cli.run()


if __name__ == "__main__":
    main()
