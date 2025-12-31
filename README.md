
# 🌿 PlantFormulatorAI | Master Class Edition
**The "Senior Scientist" AI for Plant-Based Food R&D**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Science](https://img.shields.io/badge/Food%20Science-Rheology-green) ![Visualization](https://img.shields.io/badge/Matplotlib-Radar%20Charts-orange) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

**PlantFormulatorAI** is a specialized Machine Learning application designed to act as a **Senior R&D Partner** for food technologists. Unlike simple calculators, this AI explains the *science* behind every formulation decision, predicts rheological outcomes (texture/stability), and visualizes sensory profiles before you ever step into the lab.

---

## ✨ Key Capabilities

### 🎓 **Hyper-Detailed "Professor" Mode**
The AI doesn't just ask for numbers; it teaches you *why* they matter.
* **Contextual Education:** Explains how fat globules mask astringency or why pH near 4.5 causes protein crashing.
* **Deep Analysis:** Instead of a simple score, it generates a full paragraph analyzing the chemical stability of your specific matrix.

### 🔬 **Physicochemical Simulation Engine**
* **Random Forest Modeling:** Trained on synthetic datasets representing protein solubility, water holding capacity (WHC), and hydrocolloid interactions.
* **Dynamic Learning:** You can teach the AI new ingredients (e.g., "Mung Bean Isolate") by inputting their lab specs (WHC & Solubility), and it retrains itself instantly.

### 📊 **Visual Sensory Lab**
* **Radar Charts (Spider Plots):** Real-time visualization of the trade-offs in your recipe:
    * **Texture:** (Viscosity/Mouthfeel)
    * **Stability:** (Risk of Syneresis/Separation)
    * **Cost:** (Raw Material Efficiency)
    * **Nutrition:** (Protein Density)

### 🗂 **Digital Lab Notebook**
* **Auto-Archiving:** Every experiment is saved to a local or cloud-synced JSON database.
* **Pin & Organize:** Pin 📌 your "Gold Standard" recipes to the top of the list.
* **Recall:** Click any past experiment to reload its data and charts for comparison.

---

## 🛠️ Installation Guide

### Prerequisites
* **Python 3.x** installed on your system.

### 1. Install Libraries
Open your Command Prompt (Windows) or Terminal (Mac/Linux) and run this single command to install the AI and Charting tools:

```bash
pip install pandas numpy scikit-learn matplotlib

```

### 2. Launch the App

Navigate to the folder where you saved the code and run:

```bash
python PlantBotMaster.py

```

---

## 📖 User Tutorial: Running an Experiment

### Scenario: Creating a High-Protein Pea Yogurt

*You want to see if a Pea Protein isolate will be stable at a yogurt pH (4.5).*

**Step 1: Initialization**

* **User:** Types `New` in the chat.
* **Bot:** Explains that protein source determines water absorption kinetics and asks you to choose a substrate (Pea, Soy, Oat, etc.).

**Step 2: Defining the Matrix**

* **User:** Types `Pea`.
* **Bot:** Confirms selection and asks for **Protein Concentration**. It explains that 2-4% is milk-like, while 5-10% is spoonable.
* **User:** Types `8.5` (Targeting a thick Greek style).

**Step 3: Adjusting Mouthfeel**

* **Bot:** Asks for **Fat Content**, explaining that fat is needed to coat the tongue and reduce plant grit.
* **User:** Types `3.0` (Coconut oil).

**Step 4: The Critical pH Step**

* **Bot:** Asks for **pH Level**, warning that plant proteins have an *Isoelectric Point* (usually pH 4.5) where they lose charge and precipitate.
* **User:** Types `4.5`.

**Step 5: Stabilization**

* **Bot:** Asks for **Stabilizer %** (Pectin/Starch) to manage free water.
* **User:** Types `0.4`.

**Step 6: The Analysis**

* **Bot:** Runs the Random Forest model.
* **Output:**
* **Score:** 82/100 (Premium Structure).
* **Report:** *"The model predicts a highly stable, cohesive gel network. The protein concentration and pH are perfectly aligned..."*
* **Visual:** The Radar Chart on the right updates to show high Texture scores but moderate Cost efficiency.



---

## 🧪 Scientific Glossary

The AI uses specific food science metrics. Here is a cheat sheet:

| Metric | Definition | Impact on AI Model |
| --- | --- | --- |
| **WHC (Water Holding Capacity)** | Grams of water bound per gram of protein. | **High WHC** = Thicker texture, less separation. |
| **Solubility Index (NSI)** | % of protein that dissolves at neutral pH. | **Low Solubility** = Gritty/Sandy mouthfeel. **High** = Smooth milk. |
| **Isoelectric Point (pI)** | The pH where protein has net zero charge. | If pH is near pI (approx 4.5) without stabilizers, the score drops (crashing). |
| **Syneresis** | The expulsion of liquid (whey) from a gel. | The AI penalizes recipes with low stabilizer + low solid content. |

---

## 📦 How to Create a Standalone .EXE

Want to send this to a colleague who doesn't have Python?

1. **Install PyInstaller:**
```bash
pip install pyinstaller

```


2. **Compile the App:**
```bash
pyinstaller --noconfirm --onefile --windowed --name "PlantBotMaster" PlantBotMaster.py

```


3. **Distribute:**
Go to the `dist/` folder. You will find `PlantBotMaster.exe`. You can email this file to your team.

---

## 📝 License

This project is open-source under the **MIT License**.

* **You are free to:** Modify, distribute, and use for commercial R&D.
* **Disclaimer:** This tool uses synthetic data for simulation. Always validate final formulations with physical bench testing (Rheometer/Viscometer).

```

```
