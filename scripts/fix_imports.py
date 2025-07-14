#!/usr/bin/env python3
"""
Comprehensive Import Fix Script
Fix missing imports across all intelligence components
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix missing imports in a Python file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file needs timedelta import
        needs_timedelta = 'timedelta' in content and 'from datetime import timedelta' not in content
        needs_datetime = 'datetime' in content and 'from datetime import datetime' not in content
        
        if needs_timedelta or needs_datetime:
            print(f"🔧 Fixing imports in: {file_path}")
            
            # Find existing datetime imports
            datetime_import_pattern = r'from datetime import ([^\n]+)'
            match = re.search(datetime_import_pattern, content)
            
            if match:
                # Update existing import
                current_imports = match.group(1)
                new_imports = []
                
                if 'datetime' not in current_imports:
                    new_imports.append('datetime')
                else:
                    new_imports.extend([x.strip() for x in current_imports.split(',') if x.strip()])
                
                if 'timedelta' not in current_imports and needs_timedelta:
                    new_imports.append('timedelta')
                
                # Remove duplicates while preserving order
                seen = set()
                unique_imports = []
                for imp in new_imports:
                    if imp not in seen:
                        unique_imports.append(imp)
                        seen.add(imp)
                
                new_import_line = f"from datetime import {', '.join(unique_imports)}"
                content = re.sub(datetime_import_pattern, new_import_line, content)
                
            else:
                # Add new import at the top, after other imports
                import_lines = []
                if needs_datetime:
                    import_lines.append('datetime')
                if needs_timedelta:
                    import_lines.append('timedelta')
                
                new_import = f"from datetime import {', '.join(import_lines)}"
                
                # Find a good place to insert the import
                lines = content.split('\n')
                insert_index = 0
                
                # Find the best position after existing imports but before code
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        insert_index = i + 1
                    elif line.strip() and not line.startswith('#'):
                        break
                
                lines.insert(insert_index, new_import)
                content = '\n'.join(lines)
            
            # Write the fixed content back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed imports in: {file_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix imports across all intelligence components"""
    
    print("🔧 COMPREHENSIVE IMPORT FIX")
    print("=" * 40)
    print("Scanning and fixing missing datetime imports...")
    print()
    
    # Files that commonly need datetime imports
    files_to_check = [
        "python-backend/api_server.py",
        "analysis/business.py",
        "analysis/strategic.py", 
        "analysis/projects.py",
        "core/extractors.py",
        "scripts/database_direct_connection.py",
        "scripts/database_diagnostics.py"
    ]
    
    # Add any Python files in the analysis directory
    analysis_dir = Path("analysis")
    if analysis_dir.exists():
        for py_file in analysis_dir.glob("*.py"):
            if str(py_file) not in files_to_check:
                files_to_check.append(str(py_file))
    
    fixed_count = 0
    checked_count = 0
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            checked_count += 1
            if fix_imports_in_file(file_path):
                fixed_count += 1
        else:
            print(f"⚠️ File not found: {file_path}")
    
    print(f"\n📊 IMPORT FIX SUMMARY")
    print("=" * 25)
    print(f"Files checked: {checked_count}")
    print(f"Files fixed: {fixed_count}")
    
    if fixed_count > 0:
        print("\n🎯 NEXT STEPS:")
        print("1. Restart your API server:")
        print("   cd python-backend && python start_server.py")
        print("2. Test the chat again with: 'What's our revenue pipeline?'")
        print("3. You should now see real strategic intelligence!")
    else:
        print("\n✅ All imports appear to be correct")
        print("💡 The issue might be elsewhere - let's debug further")

if __name__ == "__main__":
    main()