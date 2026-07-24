import os
from Bio.PDB import PDBList
import pymol
from pymol import cmd

def run_bioinformatics_pipeline(pdb_id):
    print(f"=== [Step 1] 开始从 NCBI/PDB 数据库自动化下载结构: {pdb_id} ===")
    pdbl = PDBList()
    local_file = pdbl.retrieve_pdb_file(pdb_id, pdir='.', file_format='pdb')
    
    standard_name = f"{pdb_id.lower()}.pdb"
    if os.path.exists(f"pdb{pdb_id.lower()}.ent"):
        os.rename(f"pdb{pdb_id.lower()}.ent", standard_name)
    
    print(f"=== [Step 2] 成功获取本地文件: {standard_name} ===")
    print("=== [Step 3] 启动后台静默 PyMOL 引擎进行 3D 渲染 ===")
    
    # 初始化 PyMOL 后台静默运行模式
    pymol.pymol_argv = ['pymol', '-qc'] 
    pymol.finish_launching()
    
    # 执行 PyMOL 核心制图指令
    cmd.load(standard_name, "protein")          
    cmd.show_as("cartoon", "protein")          
    cmd.color("marine", "protein")           
    cmd.bg_color("white")                      
    
    cmd.orient()
    output_png = f"{pdb_id.lower()}_structure.png"
    cmd.ray(1200, 900)                         
    cmd.png(output_png)                        
    
    print(f"🎉 Pipeline 执行成功！科研插图已保存为: {output_png}")
    cmd.quit()

if __name__ == "__main__":
    # 以经典的 6VSB (新冠病毒 Spike 突起蛋白结构) 为例进行测试
    run_bioinformatics_pipeline("6VSB")
