"""SmartAttend - Quick Start Launcher"""
import os
import sys

print("=" * 50)
print("  SmartAttend - Quick Start")
print("=" * 50)
print()
print("Choose backend to run:")
print("1. Minimal Backend (in-memory, single file)")
print("2. Full Backend (structured Flask + JWT, all features)")
print()

choice = input("Enter choice (1 or 2): ").strip()

if choice == "2":
    print("\n Starting full backend...")
    os.system(f"{sys.executable} backend/run.py")
else:
    print("\n Starting minimal backend...")
    os.system(f"{sys.executable} backend/app_minimal.py")
