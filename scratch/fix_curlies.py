# coding: utf-8
import os
import glob

# In the 10 files, let's fix single curlies that should be double curlies
for filepath in glob.glob('pages/payment-app-dir*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If it was generated via f-string, let's check for single-curly Vue expressions
    # Let's inspect where it happens
    # Actually, let's re-run the generator with proper replacement!
print("Glob check ready.")
