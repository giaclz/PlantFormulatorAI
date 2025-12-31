# PlantFormulator AI 🌿🧪
**Machine Learning for Next-Gen Plant-Based Product Development**

![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Platform](https://img.shields.io/badge/platform-windows-lightgrey)

**PlantFormulator AI** is a desktop application designed to accelerate Research & Development (R&D) for plant-based food products. By leveraging Machine Learning (Random Forest Regression), it predicts the texture and stability of dairy alternatives (e.g., yogurts, creams) based on ingredient physicochemical properties—drastically reducing the need for trial-and-error bench testing.

---

## 🚀 Key Features

* **📈 AI-Powered Prediction:** Uses a Random Forest Regressor to predict a "Texture Score" based on complex ingredient interactions.
* **🧬 Physicochemical Modeling:** Inputs go beyond simple names, factoring in Protein Concentration, Water Holding Capacity (WHC), Solubility Index, pH, and Fat Content.
* **🧪 Synthetic Lab Simulation:** Includes a built-in synthetic data generator that simulates 2,000+ formulations to train the model instantly without requiring proprietary datasets.
* **🖥️ User-Friendly GUI:** A clean Windows-native interface built with `tkinter`—no coding knowledge required for end-users.
* **💾 Recipe Export:** Save your high-scoring formulations directly to CSV/Excel for lab verification.
* **⚡ Portable Executable:** Can be compiled into a standalone `.exe` to run on any Windows machine without Python installed.

---

## ⚙️ How It Works

1.  **Initialization:** Upon launch, the app generates a synthetic dataset representing physical lab tests (protein solubility curves, gelation points, etc.) and trains the ML model in real-time.
2.  **Input:** The food scientist inputs formulation parameters (e.g., "Pea Protein", "pH 4.6", "0.5% Stabilizer").
3.  **Inference:** The model predicts a Texture Score (0-100) by analyzing non-linear relationships between the ingredients.
4.  **Optimization:** The user adjusts sliders to maximize the score before heading to the physical lab.
5.  **Export:** Promising recipes are saved to a CSV file for the lab team.

---

## 📦 Installation & Usage

You can run this application directly from the Python source code or build it as a standalone Windows executable.

### Option 1: Run from Source (For Developers)

**Prerequisites:** Python 3.x installed.

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/PlantFormulatorAI.git](https://github.com/YOUR_USERNAME/PlantFormulatorAI.git)
    cd PlantFormulatorAI
    ```

2.  Install dependencies:
    ```bash
    pip install pandas numpy scikit-learn
    ```

3.  Run the application:
    ```bash
    python PlantApp.py
    ```

### Option 2: Build Standalone .exe (For Distribution)

To create a portable file that runs on any Windows computer (no Python required):

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2.  Build the executable:
    ```bash
    pyinstaller --noconfirm --onefile --windowed --name "PlantFormulatorAI" PlantApp.py
    ```

3.  Locate the app:
    Go to the `dist/` folder. You will find `PlantFormulatorAI.exe`.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** Tkinter (Standard Library)
* **Machine Learning:** Scikit-Learn (Random Forest Regressor)
* **Data Processing:** Pandas, NumPy
* **Deployment:** PyInstaller

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for better physicochemical features or model improvements:

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/NewFeature`)
3.  Commit your Changes (`git commit -m 'Add some NewFeature'`)
4.  Push to the Branch (`git push origin feature/NewFeature`)
5.  Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### ⚠️ Disclaimer
*This tool uses synthetic data for demonstration purposes to simulate R&D workflows. For commercial application, the model code should be retrained on actual rheological data specific to your proprietary ingredients.*
