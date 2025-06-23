# BookMinder Distribution Guide

This guide covers how to package and distribute BookMinder for end users, from technical users comfortable with command lines to consumers expecting native applications.

## For Technical Users (PyPI)

The traditional Python approach - publish to the Python Package Index:

Build and publish:
```bash
uv build
uv publish
```

Users install with pipx (ideal for CLI tools as it creates isolated environments):
```bash
pipx install bookminder
bookminder list recent
```

## For Non-Technical Users

### 1. Standalone Executables

Create a single executable file that includes Python and all dependencies.

Using PyInstaller:
```bash
pyinstaller --onefile bookminder/cli.py
```

This creates `dist/bookminder` - users can download and run without installing Python.

Using Nuitka (produces smaller, faster executables):
```bash
python -m nuitka --onefile --follow-imports bookminder/cli.py
```

### 2. macOS App Bundle

Create a native macOS application using py2app.

Create setup.py:
```python
from setuptools import setup

setup(
    app=['bookminder/cli.py'],
    options={
        'py2app': {
            'packages': ['bookminder'],
            'plist': {
                'CFBundleName': 'BookMinder',
                'CFBundleDisplayName': 'BookMinder',
                'CFBundleIdentifier': 'com.example.bookminder',
                'CFBundleVersion': '1.0.0',
                'CFBundleShortVersionString': '1.0.0',
            }
        }
    },
    setup_requires=['py2app'],
)
```

Build the app:
```bash
python setup.py py2app
```

Creates `BookMinder.app` that users can drag to Applications folder.

### 3. Homebrew Formula

Many macOS developers prefer installing via Homebrew.

Create a formula:
```ruby
class Bookminder < Formula
  desc "Extract content and highlights from Apple Books"
  homepage "https://github.com/palimondo/BookMinder"
  url "https://github.com/palimondo/BookMinder/archive/v1.0.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"
  license "MIT"
  
  depends_on "python@3.13"
  
  def install
    virtualenv_install_with_resources
  end
  
  test do
    system "#{bin}/bookminder", "--version"
  end
end
```

Users install with:
```bash
brew tap palimondo/bookminder
brew install bookminder
```

### 4. Modern Python Apps (PEX/Shiv)

Create self-contained Python executables that include all dependencies.

Using shiv:
```bash
shiv -c bookminder -o bookminder.pyz bookminder
```

Users run with:
```bash
python bookminder.pyz list recent
```

Or make it fully executable:
```bash
echo '#!/usr/bin/env python' | cat - bookminder.pyz > bookminder
chmod +x bookminder
./bookminder list recent
```

### 5. Native GUI Wrapper

For a full GUI application, use Briefcase or Flet.

Using Briefcase:
```bash
briefcase new
briefcase create
briefcase build
briefcase package --macOS
```

This creates a native macOS app with Python embedded, complete with code signing and notarization support.

## Distribution Strategy for BookMinder

Given BookMinder's nature as a macOS-only tool accessing Apple Books:

### Recommended Approach

1. **Primary Distribution**: Homebrew
   - Most macOS developers already use it
   - Easy updates via `brew upgrade`
   - Handles Python dependency automatically

2. **Secondary Distribution**: Standalone Executable
   - For users who don't use Homebrew
   - PyInstaller with code signing for security
   - Distribute via GitHub Releases

3. **Future Enhancement**: Native GUI
   - If adding graphical interface
   - Use Briefcase for native macOS experience
   - Distribute via Mac App Store or direct download

### Implementation Priority

1. Start with PyPI + pipx for early adopters
2. Add Homebrew formula once stable
3. Create standalone executable for wider audience
4. Consider GUI wrapper if user demand exists

## Key Considerations

- **Code Signing**: Required for macOS distribution to avoid security warnings
- **Notarization**: Apple requires this for apps distributed outside App Store
- **Auto-Updates**: Consider using Sparkle framework for standalone apps
- **Python Version**: Bundle Python 3.13 to ensure compatibility

## Conclusion

Modern Python tooling (uv, pipx) makes development smooth, but distribution still requires platform-specific packaging. Choose based on your target audience:

- Developers: PyPI + Homebrew
- Power Users: Standalone executable
- General Users: Native app bundle

The beauty of the modern Python ecosystem is you can start simple (PyPI) and gradually add more distribution methods as your user base grows.