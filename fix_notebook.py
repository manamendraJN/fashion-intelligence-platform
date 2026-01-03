import json
import os
from pathlib import Path

def find_notebooks():
    """Find all .ipynb files in current directory and subdirectories"""
    notebooks = []
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"\n📁 Searching in: {current_dir}")
    
    # Walk through all directories
    for root, dirs, files in os.walk(current_dir):
        # Skip hidden and checkpoint directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and 'checkpoint' not in d. lower()]
        
        for file in files:
            if file.endswith('.ipynb') and 'checkpoint' not in file.lower():
                full_path = os.path.join(root, file)
                notebooks.append(full_path)
    
    return notebooks

def fix_notebook(notebook_path):
    """Remove widget metadata from notebook"""
    print(f"\n📖 Processing:  {notebook_path}")
    
    try:
        # Load notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # Remove widgets metadata
        if 'metadata' in nb and 'widgets' in nb['metadata']:
            del nb['metadata']['widgets']
            print("✅ Removed widgets metadata")
            
            # Save fixed notebook
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=1, ensure_ascii=False)
            
            print(f"✅ Fixed and saved: {notebook_path}")
            print("📁 All outputs preserved!")
            return True
        else:
            print("⚠️  No widgets metadata found (notebook might be clean already)")
            return False
            
    except Exception as e:
        print(f"❌ Error:  {e}")
        return False

def main():
    print("="*70)
    print("NOTEBOOK WIDGET METADATA FIXER")
    print("="*70)
    
    # Find all notebooks
    notebooks = find_notebooks()
    
    if not notebooks:
        print("\n❌ No . ipynb files found!")
        print("\n💡 Make sure you have . ipynb files in this directory or subdirectories")
        print(f"📁 Current directory: {os.getcwd()}")
        return
    
    print(f"\n📚 Found {len(notebooks)} notebook(s):")
    for i, nb in enumerate(notebooks, 1):
        # Show relative path
        rel_path = os.path.relpath(nb)
        print(f"   {i}. {rel_path}")
    
    # If only one notebook, fix it automatically
    if len(notebooks) == 1:
        print(f"\n🔧 Fixing the only notebook found...")
        fix_notebook(notebooks[0])
    else:
        # Let user choose
        print(f"\n🔧 Which notebook do you want to fix? ")
        print("   0. Fix ALL notebooks")
        for i, nb in enumerate(notebooks, 1):
            rel_path = os.path.relpath(nb)
            print(f"   {i}. {rel_path}")
        
        try: 
            choice = input("\nEnter number (or 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                print("👋 Exiting...")
                return
            
            choice = int(choice)
            
            if choice == 0:
                # Fix all
                print(f"\n🔧 Fixing ALL {len(notebooks)} notebooks...")
                fixed_count = 0
                for nb in notebooks:
                    if fix_notebook(nb):
                        fixed_count += 1
                print(f"\n✅ Fixed {fixed_count}/{len(notebooks)} notebooks")
            elif 1 <= choice <= len(notebooks):
                # Fix selected
                fix_notebook(notebooks[choice - 1])
            else:
                print("❌ Invalid choice!")
        except ValueError:
            print("❌ Invalid input!")
        except KeyboardInterrupt:
            print("\n\n👋 Cancelled by user")
    
    print("\n" + "="*70)
    print("DONE!  You can now commit and push to GitHub")
    print("="*70)

if __name__ == '__main__':
    main()