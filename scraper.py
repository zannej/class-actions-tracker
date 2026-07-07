import os

print("Files in current directory:")
os.system('ls -la')

print("\nChecking for credentials.json:")
if os.path.exists('credentials.json'):
    print("✓ credentials.json EXISTS")
    with open('credentials.json', 'r') as f:
        content = f.read()
    print(f"✓ File size: {len(content)} bytes")
    print(f"✓ First 100 characters: {content[:100]}")
else:
    print("✗ credentials.json NOT FOUND")
