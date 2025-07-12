import tkinter as tk
from tkinter import ttk, messagebox

class MoyersAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Moyer's Mixed Dentition Analysis")
        self.root.geometry("800x600")
        
        # Create notebook for lower and upper arch tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Lower Arch Frame
        self.lower_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.lower_frame, text='Lower Arch Analysis')
        
        # Upper Arch Frame
        self.upper_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.upper_frame, text='Upper Arch Analysis')
        
        # Initialize both arch interfaces
        self.create_lower_arch_interface()
        self.create_upper_arch_interface()
        
        # Add info button
        info_button = ttk.Button(root, text="About Moyer's Analysis", command=self.show_info)
        info_button.pack(pady=5)
    
    def create_lower_arch_interface(self):
        # Title
        ttk.Label(self.lower_frame, text="Lower Arch Analysis", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Measurement inputs
        ttk.Label(self.lower_frame, text="Mandibular Incisors Sum (mm):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.lower_incisors_sum = tk.DoubleVar(value=22.0)
        ttk.Entry(self.lower_frame, textvariable=self.lower_incisors_sum, width=10).grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(self.lower_frame, text="Space Available (mm):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.lower_space_available = tk.DoubleVar(value=25.0)
        ttk.Entry(self.lower_frame, textvariable=self.lower_space_available, width=10).grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Calculate button
        ttk.Button(self.lower_frame, text="Calculate", command=self.calculate_lower).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Results frame
        self.lower_results_frame = ttk.LabelFrame(self.lower_frame, text="Results")
        self.lower_results_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='ew')
        
        # Table for predicted values (75% level)
        ttk.Label(self.lower_frame, text="Moyer's Prediction Table (75% probability level)").grid(row=5, column=0, columnspan=4, pady=5)
        
        self.lower_table = ttk.Treeview(self.lower_frame, columns=('sum_incisors', 'canine', 'premolars'), show='headings', height=5)
        self.lower_table.heading('sum_incisors', text='Sum of Incisors (mm)')
        self.lower_table.heading('canine', text='Canine (mm)')
        self.lower_table.heading('premolars', text='Premolars (mm)')
        self.lower_table.column('sum_incisors', width=150, anchor='center')
        self.lower_table.column('canine', width=100, anchor='center')
        self.lower_table.column('premolars', width=100, anchor='center')
        self.lower_table.grid(row=6, column=0, columnspan=4, padx=10, pady=5)
        
        # Populate the table with standard values
        self.populate_lower_table()
        
        # Inference text
        self.lower_inference = tk.Text(self.lower_frame, height=8, width=80, wrap='word')
        self.lower_inference.grid(row=7, column=0, columnspan=4, padx=10, pady=10)
        
        # Add scrollbar to inference text
        scrollbar = ttk.Scrollbar(self.lower_frame, command=self.lower_inference.yview)
        scrollbar.grid(row=7, column=4, sticky='ns')
        self.lower_inference.config(yscrollcommand=scrollbar.set)
    
    def populate_lower_table(self):
        # Standard values from Moyer's analysis at 75% probability level
        data = [
            (20.0, 6.5, 10.5),
            (21.0, 6.6, 10.7),
            (22.0, 6.7, 10.9),
            (23.0, 6.8, 11.1),
            (24.0, 6.9, 11.3),
            (25.0, 7.0, 11.5),
            (26.0, 7.1, 11.7),
            (27.0, 7.2, 11.9),
            (28.0, 7.3, 12.1),
            (29.0, 7.4, 12.3),
            (30.0, 7.5, 12.5)
        ]
        
        for item in data:
            self.lower_table.insert('', 'end', values=item)
    
    def calculate_lower(self):
        try:
            incisors_sum = float(self.lower_incisors_sum.get())
            space_available = float(self.lower_space_available.get())
            
            if incisors_sum < 20 or incisors_sum > 30:
                messagebox.showerror("Error", "Sum of mandibular incisors should be between 20-30mm")
                return
                
            if space_available <= 0:
                messagebox.showerror("Error", "Space available must be positive")
                return
            
            # Get predicted values (using linear approximation from the table)
            # For simplicity, we'll use the formula: predicted = 0.1 * incisors_sum + 4.5 (for premolars)
            predicted_canine = 0.1 * incisors_sum + 4.5
            predicted_premolars = 0.2 * incisors_sum + 6.5
            total_space_required = predicted_canine + predicted_premolars
            
            # Calculate discrepancy
            discrepancy = space_available - total_space_required
            
            # Generate inference
            inference_text = f"Analysis Results:\n"
            inference_text += f"- Sum of mandibular incisors: {incisors_sum:.1f} mm\n"
            inference_text += f"- Predicted canine width: {predicted_canine:.1f} mm\n"
            inference_text += f"- Predicted premolars width: {predicted_premolars:.1f} mm\n"
            inference_text += f"- Total predicted space required: {total_space_required:.1f} mm\n"
            inference_text += f"- Space available: {space_available:.1f} mm\n"
            inference_text += f"- Discrepancy: {discrepancy:.1f} mm\n\n"
            
            if discrepancy > 2:
                inference_text += "Interpretation: Significant space excess (>2mm). Consider:\n"
                inference_text += "- Monitoring for spacing issues\n"
                inference_text += "- Possible prosthetic replacement if excessive\n"
            elif discrepancy > 0:
                inference_text += "Interpretation: Mild space excess (0-2mm). Usually acceptable.\n"
            elif discrepancy == 0:
                inference_text += "Interpretation: Perfect space match. Ideal situation.\n"
            elif discrepancy > -3:
                inference_text += "Interpretation: Mild space deficiency (0-3mm). Consider:\n"
                inference_text += "- Interproximal reduction if minimal\n"
                inference_text += "- Monitoring eruption pattern\n"
            else:
                inference_text += "Interpretation: Significant space deficiency (>3mm). Consider:\n"
                inference_text += "- Extraction treatment plan\n"
                inference_text += "- Distalization if appropriate\n"
                inference_text += "- Expansion if indicated (limited in mandible)\n"
            
            self.lower_inference.delete(1.0, tk.END)
            self.lower_inference.insert(tk.END, inference_text)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values")
    
    def create_upper_arch_interface(self):
        # Title
        ttk.Label(self.upper_frame, text="Upper Arch Analysis", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Measurement inputs
        ttk.Label(self.upper_frame, text="Mandibular Incisors Sum (mm):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.upper_incisors_sum = tk.DoubleVar(value=22.0)
        ttk.Entry(self.upper_frame, textvariable=self.upper_incisors_sum, width=10).grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(self.upper_frame, text="Space Available (mm):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.upper_space_available = tk.DoubleVar(value=32.0)
        ttk.Entry(self.upper_frame, textvariable=self.upper_space_available, width=10).grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(self.upper_frame, text="Current Overjet (mm):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.overjet = tk.DoubleVar(value=3.0)
        ttk.Entry(self.upper_frame, textvariable=self.overjet, width=10).grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(self.upper_frame, text="Target Overjet (mm):").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.target_overjet = tk.DoubleVar(value=2.0)
        ttk.Entry(self.upper_frame, textvariable=self.target_overjet, width=10).grid(row=4, column=1, padx=5, pady=5, sticky='w')
        
        # Calculate button
        ttk.Button(self.upper_frame, text="Calculate", command=self.calculate_upper).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Results frame
        self.upper_results_frame = ttk.LabelFrame(self.upper_frame, text="Results")
        self.upper_results_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky='ew')
        
        # Table for predicted values (75% level)
        ttk.Label(self.upper_frame, text="Moyer's Prediction Table for Maxillary Teeth (75% probability level)").grid(row=7, column=0, columnspan=4, pady=5)
        
        self.upper_table = ttk.Treeview(self.upper_frame, columns=('sum_incisors', 'canine', 'premolars'), show='headings', height=5)
        self.upper_table.heading('sum_incisors', text='Sum of Mand. Incisors (mm)')
        self.upper_table.heading('canine', text='Canine (mm)')
        self.upper_table.heading('premolars', text='Premolars (mm)')
        self.upper_table.column('sum_incisors', width=150, anchor='center')
        self.upper_table.column('canine', width=100, anchor='center')
        self.upper_table.column('premolars', width=100, anchor='center')
        self.upper_table.grid(row=8, column=0, columnspan=4, padx=10, pady=5)
        
        # Populate the table with standard values
        self.populate_upper_table()
        
        # Inference text
        self.upper_inference = tk.Text(self.upper_frame, height=8, width=80, wrap='word')
        self.upper_inference.grid(row=9, column=0, columnspan=4, padx=10, pady=10)
        
        # Add scrollbar to inference text
        scrollbar = ttk.Scrollbar(self.upper_frame, command=self.upper_inference.yview)
        scrollbar.grid(row=9, column=4, sticky='ns')
        self.upper_inference.config(yscrollcommand=scrollbar.set)
    
    def populate_upper_table(self):
        # Standard values from Moyer's analysis at 75% probability level for maxillary teeth
        data = [
            (20.0, 7.0, 11.0),
            (21.0, 7.2, 11.2),
            (22.0, 7.4, 11.4),
            (23.0, 7.6, 11.6),
            (24.0, 7.8, 11.8),
            (25.0, 8.0, 12.0),
            (26.0, 8.2, 12.2),
            (27.0, 8.4, 12.4),
            (28.0, 8.6, 12.6),
            (29.0, 8.8, 12.8),
            (30.0, 9.0, 13.0)
        ]
        
        for item in data:
            self.upper_table.insert('', 'end', values=item)
    
    def calculate_upper(self):
        try:
            incisors_sum = float(self.upper_incisors_sum.get())
            space_available = float(self.upper_space_available.get())
            current_overjet = float(self.overjet.get())
            target_overjet = float(self.target_overjet.get())
            
            if incisors_sum < 20 or incisors_sum > 30:
                messagebox.showerror("Error", "Sum of mandibular incisors should be between 20-30mm")
                return
                
            if space_available <= 0:
                messagebox.showerror("Error", "Space available must be positive")
                return
                
            if current_overjet < 0 or target_overjet < 0:
                messagebox.showerror("Error", "Overjet values must be positive")
                return
            
            # Get predicted values (using linear approximation from the table)
            predicted_canine = 0.2 * incisors_sum + 3.0
            predicted_premolars = 0.2 * incisors_sum + 7.0
            total_space_required = predicted_canine + predicted_premolars
            
            # Adjust for overjet correction (each mm of overjet reduction requires about 2mm of space)
            overjet_correction = (current_overjet - target_overjet) * 2
            adjusted_space_required = total_space_required + overjet_correction
            
            # Calculate discrepancy
            discrepancy = space_available - adjusted_space_required
            
            # Generate inference
            inference_text = f"Analysis Results:\n"
            inference_text += f"- Sum of mandibular incisors: {incisors_sum:.1f} mm\n"
            inference_text += f"- Predicted canine width: {predicted_canine:.1f} mm\n"
            inference_text += f"- Predicted premolars width: {predicted_premolars:.1f} mm\n"
            inference_text += f"- Total predicted space required: {total_space_required:.1f} mm\n"
            inference_text += f"- Overjet correction space: {overjet_correction:.1f} mm\n"
            inference_text += f"- Adjusted space required: {adjusted_space_required:.1f} mm\n"
            inference_text += f"- Space available: {space_available:.1f} mm\n"
            inference_text += f"- Discrepancy: {discrepancy:.1f} mm\n\n"
            
            if discrepancy > 3:
                inference_text += "Interpretation: Significant space excess (>3mm). Consider:\n"
                inference_text += "- Monitoring for spacing issues\n"
                inference_text += "- Possible prosthetic replacement if excessive\n"
                inference_text += "- Mesial movement of posterior teeth if needed\n"
            elif discrepancy > 0:
                inference_text += "Interpretation: Mild space excess (0-3mm). Usually acceptable.\n"
            elif discrepancy == 0:
                inference_text += "Interpretation: Perfect space match. Ideal situation.\n"
            elif discrepancy > -5:
                inference_text += "Interpretation: Moderate space deficiency (0-5mm). Consider:\n"
                inference_text += "- Interproximal reduction\n"
                inference_text += "- Expansion (more feasible in maxilla than mandible)\n"
                inference_text += "- Distalization of molars if possible\n"
            else:
                inference_text += "Interpretation: Significant space deficiency (>5mm). Consider:\n"
                inference_text += "- Extraction treatment plan\n"
                inference_text += "- Comprehensive orthodontic treatment\n"
                inference_text += "- Possible orthopedic expansion if age-appropriate\n"
            
            self.upper_inference.delete(1.0, tk.END)
            self.upper_inference.insert(tk.END, inference_text)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values")
    
    def show_info(self):
        info_text = """MOYER'S MIXED DENTITION ANALYSIS

Advantages:
- Minimal systematic error
- High reliability
- Not time-consuming
- No radiographs or special equipment required
- Can be done even in mouth with reasonable accuracy
- Applicable to both arches

Why mandibular incisors?
- Erupt early during mixed dentition
- Can be measured easily and accurately
- Less variable in shape and size

Procedure in lower arch:
1. Measure M-D width of lower permanent incisors
2. Calculate space needed for their alignment
3. Measure space available on the cast
4. Use prediction table (75% level) to estimate space required

Procedure in upper arch:
1. Use different probability chart for maxillary teeth
2. Make allowance for overjet correction when measuring space requirements
"""
        messagebox.showinfo("About Moyer's Analysis", info_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MoyersAnalysisApp(root)
    root.mainloop()