# Attendance Management System

A Python-based attendance management system using face recognition.

## Features
- Face recognition-based attendance marking
- Stores attendance records in `Attendance.csv`
- Web interface (using Flask)
- Easy to add new faces for recognition

## Requirements
- Python 3.10+
- pip
- face_recognition
- dlib
- numpy
- Pillow
- Flask
- Visual Studio Build Tools (for Windows, required to build dlib)

## Installation

### 1. Install Python dependencies

Open PowerShell and run:

```powershell
pip install numpy Pillow flask face_recognition
```

> **Note:** If you encounter errors installing `face_recognition` or `dlib`, you must install Visual Studio Build Tools:
>
> 1. Download from https://visualstudio.microsoft.com/visual-cpp-build-tools/
> 2. Run the installer and select "Desktop development with C++" workload.
> 3. Complete the installation and restart your computer if prompted.

### 2. Prepare Training Images
- Add clear face images to the `Training_images/` folder. Each file should be named as the person's name (e.g., `John Doe.jpg`).

### 3. Run the Application

```powershell
python main.py
```

## Usage
- The system will start and use your webcam to recognize faces.
- Attendance will be marked in `Attendance.csv`.
- Web interface and additional features may be available depending on your implementation in `main.py`.

## Project Structure
- `main.py` - Main application file
- `Attendance.csv` - Attendance records
- `Training_images/` - Folder for training images
- `static/`, `templates/` - Web assets (if using Flask)
- `dlib/` - dlib source code (if building from source)

## Troubleshooting
- **dlib installation error:**
  - This is common on Windows. You must install Visual Studio Build Tools with the "Desktop development with C++" workload.
  - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
  - After installation, restart your computer and run `pip install face_recognition` again.
- **face_recognition not found:** Ensure all dependencies are installed with pip.
- **Webcam not detected:** Make sure your webcam is connected and accessible.
- **Still having issues?**
  - Try upgrading pip: `python -m pip install --upgrade pip`
  - Check that you are using the correct Python environment (sometimes multiple Python installations can cause confusion).

## License
This project is for educational purposes.

## Credits
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [dlib](http://dlib.net/)

## FAQ
- **Q: Can I use this on Mac or Linux?**
  - A: Yes, but installation steps for dlib/face_recognition may differ. Refer to their official documentation for platform-specific instructions.
- **Q: How do I add a new person to the system?**
  - A: Add a clear image of the person to the `Training_images/` folder, named as their full name (e.g., `Jane Doe.jpg`).
- **Q: Where is attendance data stored?**
  - A: In the `Attendance.csv` file in the project root.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss what you would like to change.

## Contact
For questions or support, please open an issue on the repository or contact the project maintainer.
