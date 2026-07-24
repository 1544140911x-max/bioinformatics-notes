
import os
import sys
from Bio.PDB import PDBList
import pymol
from pymol import cmd

# Global initialization of the headless PyMOL backend (optimized for HPC/Cloud)
def init_pymol_backend():
    print("=== [INIT] Launching silent PyMOL backend engine on Linux cluster ===")
    pymol.pymol_argv = ['pymol', '-qc'] 
    pymol.finish_launching()

# Single macromolecular structure processing workflow
def process_single_pdb(pdb_id, output_dir):
    print(f"\n🚀 ---> Processing target protein: {pdb_id} <---")
    
    # 1. Automated data fetching from NCBI/PDB
    pdbl = PDBList()
    local_file = pdbl.retrieve_pdb_file(pdb_id, pdir=output_dir, file_format='pdb')
    
    # 2. File normalization and path adaptation
    raw_name = os.path.join(output_dir, f"pdb{pdb_id.lower()}.ent")
    standard_name = os.path.join(output_dir, f"{pdb_id.lower()}.pdb")
    
    if os.path.exists(raw_name):
        os.rename(raw_name, standard_name)
    
    # 3. Silent 3D molecular rendering via PyMOL API
    try:
        cmd.reinitialize() # Clear previous structures to ensure reproducibility
        cmd.load(standard_name, "protein")          
        cmd.show_as("cartoon", "protein")          
        cmd.color("marine", "protein")           
        cmd.bg_color("white")                      
        cmd.orient()
        
        output_png = os.path.join(output_dir, f"{pdb_id.lower()}_structure.png")
        cmd.ray(1200, 900) # High-resolution ray-tracing                   
        cmd.png(output_png)                        
        print(f"✅ {pdb_id} successfully rendered: {output_png}")
    except Exception as e:
        print(f"❌ Error rendering {pdb_id}: {str(e)}")

# High-throughput batch processing controller
def run_high_throughput_pipeline(list_file):
    if not os.path.exists(list_file):
        print(f"Error: Target configuration file {list_file} not found.")
        return

    output_dir = "rendered_results"
    os.makedirs(output_dir, exist_ok=True)

    # Load processing targets
    with open(list_file, 'r') as f:
        pdb_ids = [line.strip().upper() for line in f if line.strip()]
    
    print(f"📊 Task configuration loaded. Detected {len(pdb_ids)} targets for high-throughput rendering.")
    
    init_pymol_backend()
    
    # Execute batch loop
    for index, pdb_id in enumerate(pdb_ids, 1):
        print(f"\n[Progress: {index}/{len(pdb_ids)}]")
        process_single_pdb(pdb_id, output_dir)
        
    cmd.quit()
    print("\n🎉 === All high-throughput workflows completed successfully. Data archived === 🎉")

if __name__ == "__main__":
    run_high_throughput_pipeline("pdb_list.txt")
