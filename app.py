import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import os
import json
import datetime
import uuid

# --- VISUALIZATION LIBRARY ---
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- 🎨 PRO PALETTE ---
COLORS = {
    "green_accent": "#C1D37F",   
    "dark_brown": "#664E4C",     
    "beige_dark": "#E2D58B",     
    "beige_light": "#F0E2A3",    
    "peach": "#F9D4BB",          
    "red_soft": "#E5989B",       
    "white": "#FFFFFF",
    "off_white": "#FAFAFA"
}

# ==========================================
# 1. VISUALIZATION ENGINE
# ==========================================
class VisualizationManager:
    def create_radar_chart(self, parent_frame, data_dict):
        for widget in parent_frame.winfo_children(): widget.destroy()
        
        labels = list(data_dict.keys())
        stats = list(data_dict.values())
        stats = np.concatenate((stats,[stats[0]]))
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        angles = np.concatenate((angles,[angles[0]]))

        fig = plt.figure(figsize=(4, 4), facecolor=COLORS["white"])
        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, stats, 'o-', linewidth=2, color=COLORS["dark_brown"])
        ax.fill(angles, stats, alpha=0.25, color=COLORS["green_accent"])
        ax.set_thetagrids(angles[:-1] * 180/np.pi, labels, fontsize=8)
        ax.set_facecolor(COLORS["off_white"])
        ax.spines['polar'].set_visible(False)
        ax.set_yticklabels([])
        ax.grid(True, color=COLORS["beige_dark"], linestyle='--')

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

# ==========================================
# 2. STORAGE MANAGER
# ==========================================
class StorageManager:
    def __init__(self):
        self.mode = "LOCAL"
        self.base_path = os.getcwd()
        self.history_file = "plantbot_history_named.json"
        self.ingredients_file = "plantbot_ingredients.json"
        
    def set_mode(self, mode, path=None):
        self.mode = mode
        if path: self.base_path = path
        if not os.path.exists(self.base_path):
            try: os.makedirs(self.base_path)
            except: pass

    def load_ingredients(self):
        full_path = os.path.join(self.base_path, self.ingredients_file)
        if not os.path.exists(full_path):
            defaults = {
                "Pea": {"whc": 3.0, "solubility": 60, "desc": "Globulin-heavy. Earthy notes. Good gelling."},
                "Soy": {"whc": 4.5, "solubility": 85, "desc": "The gold standard. High solubility, neutral taste."},
                "Oat": {"whc": 2.5, "solubility": 40, "desc": "High starch/beta-glucan. Viscous but weak gel."},
                "Fava": {"whc": 3.5, "solubility": 55, "desc": "High foaming capacity. Can be beany."},
                "Almond": {"whc": 1.5, "solubility": 20, "desc": "Insoluble particles. Gritty if not refined."}
            }
            with open(full_path, 'w') as f: json.dump(defaults, f)
            return defaults
        with open(full_path, 'r') as f: return json.load(f)

    def save_ingredient(self, name, data):
        current = self.load_ingredients()
        current[name] = data
        with open(os.path.join(self.base_path, self.ingredients_file), 'w') as f: json.dump(current, f)

    def save_history_item(self, record, custom_name=None):
        full_path = os.path.join(self.base_path, self.history_file)
        history = self.get_history()
        
        if "id" not in record: record["id"] = str(uuid.uuid4())
        if "pinned" not in record: record["pinned"] = False
        
        # Apply custom name if provided, else default
        if custom_name:
            record["name"] = custom_name
        elif "name" not in record:
            record["name"] = f"{record['source']} Formulation"
            
        history.append(record)
        with open(full_path, 'w') as f: json.dump(history, f)
        return record["id"]

    def rename_item(self, item_id, new_name):
        history = self.get_history()
        for h in history:
            if h.get("id") == item_id:
                h["name"] = new_name
                break
        with open(os.path.join(self.base_path, self.history_file), 'w') as f: json.dump(history, f)

    def get_history(self):
        full_path = os.path.join(self.base_path, self.history_file)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f: return json.load(f)
        return []

    def delete_item(self, item_id):
        history = self.get_history()
        history = [h for h in history if h.get("id") != item_id]
        with open(os.path.join(self.base_path, self.history_file), 'w') as f: json.dump(history, f)

    def toggle_pin(self, item_id):
        history = self.get_history()
        for h in history:
            if h.get("id") == item_id: h["pinned"] = not h.get("pinned", False)
        with open(os.path.join(self.base_path, self.history_file), 'w') as f: json.dump(history, f)

# ==========================================
# 3. AI ENGINE
# ==========================================
class AIModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_columns = None

    def train(self, ingredient_db):
        data = []
        sources = list(ingredient_db.keys())
        for _ in range(2000):
            src = np.random.choice(sources)
            props = ingredient_db[src]
            conc = np.random.uniform(2, 15)
            fat = np.random.uniform(0.5, 6)
            ph = np.random.uniform(3.8, 6.5)
            stab = np.random.uniform(0.0, 1.2)
            whc = props['whc'] + np.random.normal(0, 0.2)
            sol = props['solubility'] + np.random.normal(0, 5)
            
            # Calibrated Logic
            score = (conc * 3.5) + (fat * 2.0) + (stab * 30) + (whc * 5.0)
            if ph < 4.4 and sol < 50: score -= 20
            elif ph < 4.4: score -= 10
            if sol > 80: score += 5
            score = max(0, min(100, score))
            score += np.random.normal(0, 1)
            
            data.append({'conc': conc, 'fat': fat, 'ph': ph, 'stab': stab, 'whc': whc, 'sol': sol, 'score': max(0, min(100, score)), 'source': src})
            
        df = pd.DataFrame(data)
        df_encoded = pd.get_dummies(df, columns=['source'])
        X = df_encoded.drop('score', axis=1)
        y = df['score']
        self.feature_columns = X.columns
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True

    def predict(self, inputs, source_name):
        if not self.is_trained: return 0
        input_data = pd.DataFrame([inputs])
        for col in self.feature_columns:
            if col.startswith('source_'):
                input_data[col] = 1 if col == f"source_{source_name}" else 0
            elif col not in input_data.columns:
                input_data[col] = 0
        input_data = input_data[self.feature_columns]
        X_scaled = self.scaler.transform(input_data)
        return self.model.predict(X_scaled)[0]

# ==========================================
# 4. APP UI
# ==========================================
class PlantBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PlantBot AI | Master Edition")
        self.root.geometry("1200x850")
        self.root.configure(bg=COLORS["white"])
        
        self.storage = StorageManager()
        self.ai = AIModel()
        self.visualizer = VisualizationManager()
        
        self.state = "IDLE"
        self.current_recipe = {}
        self.current_new_ing = ""
        self.temp_whc = 0.0

        self.setup_styles()
        self.build_layout()
        self.initial_training()
        self.refresh_sidebar()
        self.add_message("Bot", "🎓 **Welcome to the Lab.**\n\nI am your Senior Formulation Scientist. My job is to guide you through the complex chemistry of plant-based matrices.\n\nType **'New'** to begin an experiment. I will require precise inputs to generate a valid rheological model.")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", borderwidth=0)

    def build_layout(self):
        main = tk.Frame(self.root, bg=COLORS["white"])
        main.pack(fill='both', expand=True)

        # LEFT SIDEBAR
        sidebar = tk.Frame(main, bg=COLORS["beige_light"], width=320)
        sidebar.pack(side='left', fill='y', padx=0)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="📚 Experiment Log", bg=COLORS["dark_brown"], fg=COLORS["white"], font=("Helvetica", 12, "bold"), pady=15).pack(fill='x')
        
        self.hist_canvas = tk.Canvas(sidebar, bg=COLORS["beige_light"], highlightthickness=0)
        sb = ttk.Scrollbar(sidebar, orient="vertical", command=self.hist_canvas.yview)
        self.hist_frame = tk.Frame(self.hist_canvas, bg=COLORS["beige_light"])
        
        self.hist_frame.bind("<Configure>", lambda e: self.hist_canvas.configure(scrollregion=self.hist_canvas.bbox("all")))
        win = self.hist_canvas.create_window((0,0), window=self.hist_frame, anchor="nw", width=320)
        self.hist_canvas.bind("<Configure>", lambda e: self.hist_canvas.itemconfig(win, width=e.width))
        
        self.hist_canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.hist_canvas.configure(yscrollcommand=sb.set)

        # RIGHT CONTENT
        right = tk.Frame(main, bg=COLORS["white"])
        right.pack(side='right', fill='both', expand=True)

        # Header
        header = tk.Frame(right, bg=COLORS["dark_brown"], height=60)
        header.pack(fill='x')
        tk.Label(header, text="🌿 PlantBot AI", bg=COLORS["dark_brown"], fg=COLORS["white"], font=("Helvetica", 16, "bold")).pack(side='left', padx=20, pady=10)
        
        btn_f = tk.Frame(header, bg=COLORS["dark_brown"])
        btn_f.pack(side='right', padx=10)
        tk.Button(btn_f, text="❓ Legend", bg=COLORS["beige_dark"], command=self.open_guide, relief="flat", padx=10).pack(side='left', padx=5)
        tk.Button(btn_f, text="⚙️ Storage", bg=COLORS["green_accent"], command=self.open_storage, relief="flat", padx=10).pack(side='left', padx=5)

        # Split Area
        split = tk.Frame(right, bg=COLORS["white"])
        split.pack(fill='both', expand=True, padx=20, pady=10)

        # Chat
        self.chat_frame = tk.Frame(split, bg=COLORS["white"])
        self.chat_frame.pack(side='left', fill='both', expand=True)
        
        self.chat_cv = tk.Canvas(self.chat_frame, bg=COLORS["white"], highlightthickness=0)
        csb = ttk.Scrollbar(self.chat_frame, command=self.chat_cv.yview)
        self.chat_c_frame = tk.Frame(self.chat_cv, bg=COLORS["white"])
        
        self.chat_c_frame.bind("<Configure>", lambda e: self.chat_cv.configure(scrollregion=self.chat_cv.bbox("all")))
        cwin = self.chat_cv.create_window((0,0), window=self.chat_c_frame, anchor="nw", width=550)
        self.chat_cv.bind("<Configure>", lambda e: self.chat_cv.itemconfig(cwin, width=e.width))
        
        self.chat_cv.pack(side="left", fill="both", expand=True)
        csb.pack(side="right", fill="y")
        self.chat_cv.configure(yscrollcommand=csb.set)

        # Chart
        chart_zone = tk.Frame(split, bg=COLORS["off_white"], width=300, bd=1, relief="solid")
        chart_zone.pack(side='right', fill='y', padx=(10,0))
        tk.Label(chart_zone, text="Visual Profile", bg=COLORS["off_white"], font=("Helvetica", 10, "bold")).pack(pady=5)
        self.chart_cont = tk.Frame(chart_zone, bg=COLORS["off_white"])
        self.chart_cont.pack(fill='both', expand=True, padx=5, pady=5)

        # Input
        inp_f = tk.Frame(right, bg=COLORS["beige_dark"], height=70)
        inp_f.pack(fill='x')
        self.entry = tk.Entry(inp_f, font=("Helvetica", 12), bd=0, relief="flat")
        self.entry.pack(side='left', fill='both', expand=True, padx=15, pady=15)
        self.entry.bind("<Return>", self.send_message)
        tk.Button(inp_f, text="SUBMIT", bg=COLORS["dark_brown"], fg="white", font=("Helvetica", 10, "bold"), command=self.send_message, relief="flat", padx=20).pack(side='right', padx=15, pady=15)

    def open_guide(self):
        messagebox.showinfo("Legend", "80-100: Premium/Thick\n40-79: Standard/Pourable\n0-39: Defect/Watery")

    def open_storage(self):
        d = filedialog.askdirectory()
        if d: 
            self.storage.set_mode("CLOUD", d)
            self.refresh_sidebar()

    def refresh_sidebar(self):
        for w in self.hist_frame.winfo_children(): w.destroy()
        hist = self.storage.get_history()
        hist.sort(key=lambda x: (not x.get("pinned", False), x.get("timestamp", "")), reverse=True)
        for h in hist: self.create_card(h)

    def create_card(self, item):
        bg = COLORS["beige_dark"] if item.get("pinned") else COLORS["white"]
        c = tk.Frame(self.hist_frame, bg=bg, pady=8, padx=8)
        c.pack(fill='x', padx=10, pady=5)
        
        r1 = tk.Frame(c, bg=bg)
        r1.pack(fill='x')
        
        sc = item['score']
        col = COLORS["green_accent"] if sc>80 else (COLORS["beige_dark"] if sc>40 else COLORS["red_soft"])
        tk.Label(r1, text=f"{sc:.0f}", bg=col, width=3, font=("Arial",9,"bold")).pack(side='left')
        
        # Display NAME instead of Source
        disp_name = item.get("name", item['source'])
        if len(disp_name) > 15: disp_name = disp_name[:15] + "..."
        tk.Label(r1, text=f" {disp_name}", bg=bg, font=("Arial",10,"bold")).pack(side='left')
        
        # Actions: Rename, Delete, Pin
        tk.Button(r1, text="🗑️", bg=bg, bd=0, command=lambda: self.del_h(item['id'])).pack(side='right')
        tk.Button(r1, text="✏️", bg=bg, bd=0, command=lambda: self.rename_h(item['id'])).pack(side='right')
        tk.Button(r1, text="📌", bg=bg, bd=0, command=lambda: self.pin_h(item['id'])).pack(side='right')
        
        tk.Label(c, text=f"{item['conc']}% Prot | pH {item['ph']}", bg=bg, fg="#555", font=("Arial", 8)).pack(anchor='w')
        c.bind("<Button-1>", lambda e: self.recall(item))

    def del_h(self, iid):
        if messagebox.askyesno("Delete", "Delete this record?"):
            self.storage.delete_item(iid)
            self.refresh_sidebar()
            
    def rename_h(self, iid):
        new_name = simpledialog.askstring("Rename", "Enter new recipe name:", parent=self.root)
        if new_name:
            self.storage.rename_item(iid, new_name)
            self.refresh_sidebar()

    def pin_h(self, iid):
        self.storage.toggle_pin(iid)
        self.refresh_sidebar()
        
    def recall(self, item):
        self.add_message("Bot", f"📂 **File Retrieved:** {item.get('name', item['source'])}\nRe-loading sensory data...")
        self.update_chart(item['score'], item['stab'], item['conc'])

    def update_chart(self, score, stab, conc):
        data = {
            "Texture": score,
            "Stability": min(100, score * 1.1 if stab > 0.4 else score * 0.7),
            "Cost": max(0, 100 - (conc * 5)),
            "Nutrition": min(100, conc * 8)
        }
        self.visualizer.create_radar_chart(self.chart_cont, data)

    def add_message(self, sender, text):
        f = tk.Frame(self.chat_c_frame, bg=COLORS["white"], pady=5)
        f.pack(fill='x', padx=5)
        
        bg = COLORS["green_accent"] if sender == "Bot" else COLORS["peach"]
        align = "w" if sender == "Bot" else "e"
        av = "🤖" if sender == "Bot" else "👤"
        
        lbl = tk.Label(f, text=text, bg=bg, fg=COLORS["dark_brown"], font=("Helvetica", 10), wraplength=450, justify="left", padx=15, pady=10)
        tk.Label(f, text=av, bg=COLORS["white"], font=("Arial", 16)).pack(side=('left' if sender=="Bot" else 'right'), anchor='n', padx=5)
        lbl.pack(side=('left' if sender=="Bot" else 'right'), anchor=align)
        
        self.root.update_idletasks()
        self.chat_cv.yview_moveto(1.0)

    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if not msg: return
        self.entry.delete(0, 'end')
        self.add_message("User", msg)
        self.process_logic(msg)

    # --- SUPER DETAILED LOGIC ENGINE ---
    def process_logic(self, text):
        txt = text.lower()
        
        if self.state == "IDLE":
            if "new" in txt:
                self.state = "ASK_PROTEIN"
                ing = self.storage.load_ingredients()
                s = "\n".join([f"• {k}: {v.get('desc','')}" for k,v in ing.items()])
                self.add_message("Bot", f"🔬 **Protocol Initiated.**\n\nFirst, we must define the matrix base. The protein source dictates the isoelectric point and water absorption kinetics.\n\n**Available Substrates:**\n{s}\n\nSelect a protein or type 'Add [Name]' to characterize a new material.")
            elif txt.startswith("add "):
                self.current_new_ing = text[4:].strip().capitalize()
                self.state = "DEFINE_WHC"
                self.add_message("Bot", f"📝 **Material Characterization**\n\nWe are adding **{self.current_new_ing}** to the database.\n\nI need the **Water Holding Capacity (WHC)**.\n*Scientific Context:* This measures how many grams of water 1g of protein can bind. High WHC (>3.0) prevents syneresis (whey separation) but can create excessive viscosity.")
            else: self.add_message("Bot", "Please type **'New'** to initiate a valid experimental protocol.")

        elif self.state == "ASK_PROTEIN":
            db = self.storage.load_ingredients()
            sel = text.capitalize()
            if sel in db:
                self.current_recipe = {'source': sel, 'props': db[sel]}
                self.state = "ASK_CONC"
                self.add_message("Bot", f"✅ **Base Selected: {sel}**\n\nNow, define the **Protein Concentration (%)**.\n\n*Context:* \n• **2-4%:** Colloidal dispersion (Drinkable/Milk).\n• **5-10%:** Semi-solid gel network (Spoonable Yogurt/Cheese).\n\nWarning: Exceeding 12% without hydration control may result in chalky mouthfeel.")
            elif txt.startswith("add "):
                self.current_new_ing = text[4:].strip().capitalize()
                self.state = "DEFINE_WHC"
                self.add_message("Bot", f"📝 **New Material Entry**\n\nEnter WHC for **{self.current_new_ing}**.")
            else: self.add_message("Bot", "⚠️ **Error:** Substrate not recognized in physicochemical database.")

        elif self.state == "DEFINE_WHC":
            try:
                self.temp_whc = float(text)
                self.state = "DEFINE_SOL"
                self.add_message("Bot", "Data recorded.\n\nNext: **Solubility Index (NSI %)** (0-100).\n\n*Context:* This indicates what percentage of the protein dissolves at neutral pH. Low solubility (<40%) results in sedimentation and gritty texture ('sandiness'). High solubility (>80%) creates smooth, emulsion-stable products.")
            except: self.add_message("Bot", "Input Error: Please provide a numerical float value.")

        elif self.state == "DEFINE_SOL":
            try:
                self.storage.save_ingredient(self.current_new_ing, {"whc": self.temp_whc, "solubility": float(text), "desc": "User customized."})
                self.ai.train(self.storage.load_ingredients())
                self.state = "IDLE"
                self.add_message("Bot", f"✅ **Database Synchronized**\n\n{self.current_new_ing} has been successfully characterized and integrated into the prediction model.\nType 'New' to test it.")
            except: self.add_message("Bot", "Input Error: Numeric value required.")

        elif self.state == "ASK_CONC":
            try:
                self.current_recipe['conc'] = float(text)
                self.state = "ASK_FAT"
                self.add_message("Bot", "Concentration set.\n\nNext: **Fat Content (%)**.\n\n*Context:* Fat globules (e.g., Coconut/Sunflower oil) physically disrupt the protein gel network, making it softer and creamier. They also coat the tongue, masking the astringency of plant proteins.\n\n*Target:* 0.5% (Light) to 5.0% (Indulgent).")
            except: self.add_message("Bot", "Input Error: Numeric value required.")

        elif self.state == "ASK_FAT":
            try:
                self.current_recipe['fat'] = float(text)
                self.state = "ASK_PH"
                self.add_message("Bot", "Lipid phase defined.\n\nCRITICAL STEP: **Target pH Level**.\n\n*Context:* Plant proteins have an 'Isoelectric Point' (usually pH 4.5). If you acidify to this point, proteins lose charge and crash out, forming a gel (good for yogurt) or grit (bad for milk).\n\n• **Yogurt:** 4.3 - 4.6\n• **Milk:** 6.5 - 7.0")
            except: self.add_message("Bot", "Input Error: Numeric value required.")

        elif self.state == "ASK_PH":
            try:
                self.current_recipe['ph'] = float(text)
                self.state = "ASK_STAB"
                self.add_message("Bot", "Acidity defined.\n\nFinal Variable: **Stabilizer Dosage (%)**.\n\n*Context:* Hydrocolloids (Pectin, Starch, Agar) act as 'water managers.' They bind excess water to prevent separation (syneresis) and increase viscosity without adding calories.\n\nTypical range: 0.1% - 1.0%.")
            except: self.add_message("Bot", "Input Error: Numeric value required.")

        elif self.state == "ASK_STAB":
            try:
                self.current_recipe['stab'] = float(text)
                self.finalize()
            except: self.add_message("Bot", "Input Error: Numeric value required.")

    def finalize(self):
        r = self.current_recipe
        inputs = {'conc': r['conc'], 'fat': r['fat'], 'ph': r['ph'], 'stab': r['stab'], 'whc': r['props']['whc'], 'sol': r['props']['solubility']}
        score = self.ai.predict(inputs, r['source'])
        
        self.update_chart(score, r['stab'], r['conc'])
        
        # GENERATE DETAILED REPORT
        report = f"📊 **Final Rheological Analysis**\n\n"
        report += f"**Predicted Texture Score:** {score:.2f} / 100\n\n"
        
        if score > 80:
            report += "🏆 **Outcome: Premium Structure.**\nThe model predicts a highly stable, cohesive gel network. The protein concentration and pH are perfectly aligned to create a 'spoonable' texture similar to Greek Dairy Yogurt. Syneresis risk is minimal."
        elif score > 60:
            report += "✅ **Outcome: Standard Viscosity.**\nLikely a pourable liquid (Drinkable Yogurt/Smoothie). The matrix is stable, but lacks the solid strength of a set gel. Good mouthfeel expected."
        elif score > 40:
            report += "⚠️ **Outcome: Weak Network.**\nThe structure is fragile. You may experience phase separation (water layer on top) after 24 hours. Consider increasing the Stabilizer or protein concentration."
        else:
            report += "❌ **Outcome: Formulation Failure.**\nHigh probability of protein precipitation (grittiness) or complete separation. The pH might be too close to the isoelectric point without enough stabilizer protection."

        # NAMING DIALOG
        recipe_name = simpledialog.askstring("Save Recipe", "🧪 Formulation Complete.\n\nEnter a name for this recipe (e.g. 'Greek Style v1'):", parent=self.root)
        if not recipe_name: recipe_name = f"{r['source']} Formulation"

        self.storage.save_history_item({"timestamp": str(datetime.datetime.now()), "source": r['source'], "conc": r['conc'], "fat": r['fat'], "ph": r['ph'], "stab": r['stab'], "score": float(score)}, custom_name=recipe_name)
        self.refresh_sidebar()
        
        self.add_message("Bot", report + "\n\nData archived to Lab Notebook.")
        self.state = "IDLE"

    def initial_training(self):
        self.ai.train(self.storage.load_ingredients())

if __name__ == "__main__":
    root = tk.Tk()
    app = PlantBotUI(root)
    root.mainloop()