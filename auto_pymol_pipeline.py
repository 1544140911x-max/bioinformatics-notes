import os
import sys
from Bio.PDB import PDBList
import pymol
from pymol import cmd

# 初始化 PyMOL 静默后台引擎（全局只需启动一次，节省服务器算力和内存）
def init_pymol_backend():
    print("=== [准备阶段] 启动 Linux 算力集群后台静默 PyMOL 引擎 ===")
    pymol.pymol_argv = ['pymol', '-qc'] 
    pymol.finish_launching()

def process_single_pdb(pdb_id, output_dir):
    print(f"\n🚀 ---> 正在处理目标蛋白质: {pdb_id} <---")
    
    # 1. 自动化数据抓取
    pdbl = PDBList()
    local_file = pdbl.retrieve_pdb_file(pdb_id, pdir=output_dir, file_format='pdb')
    
    # 2. 规范文件名，适配路径
    raw_name = os.path.join(output_dir, f"pdb{pdb_id.lower()}.ent")
    standard_name = os.path.join(output_dir, f"{pdb_id.lower()}.pdb")
    
    if os.path.exists(raw_name):
        os.rename(raw_name, standard_name)
    
    # 3. 核心计算与 3D 高清渲染
    try:
        cmd.reinitialize() # 重置 PyMOL 画布，防止上一个蛋白质的结构残留影响当前渲染
        cmd.load(standard_name, "protein")          
        cmd.show_as("cartoon", "protein")          
        cmd.color("marine", "protein")           
        cmd.bg_color("white")                      
        cmd.orient()
        
        output_png = os.path.join(output_dir, f"{pdb_id.lower()}_structure.png")
        cmd.ray(1200, 900)                         
        cmd.png(output_png)                        
        print(f"✅ {pdb_id} 处理成功！高清论文插图已保存至: {output_png}")
    except Exception as e:
        print(f"❌ {pdb_id} 渲染发生错误: {str(e)}")

def run_high_throughput_pipeline(list_file):
    if not os.path.exists(list_file):
        print(f"Error: 找不到任务清单文件 {list_file}")
        return

    # 创建一个专属的输出文件夹，防止大批量文件弄脏你的 Git 根目录
    output_dir = "rendered_results"
    os.makedirs(output_dir, exist_ok=True)

    # 读取任务清单
    with open(list_file, 'r') as f:
        pdb_ids = [line.strip().upper() for line in f if line.strip()]
    
    print(f"📊 任务清单读取成功，共检测到 {len(pdb_ids)} 个蛋白质目标进行并行渲染。")
    
    # 启动后台引擎
    init_pymol_backend()
    
    # 执行高通量循环（High-Throughput Loop）
    for index, pdb_id in enumerate(pdb_ids, 1):
        print(f"\n[进度进度: {index}/{len(pdb_ids)}]")
        process_single_pdb(pdb_id, output_dir)
        
    cmd.quit()
    print("\n🎉 === 全自动化高通量生信工作流执行完毕！所有数据已安全归档 === 🎉")

if __name__ == "__main__":
    # 传入我们刚刚创建的任务目标清单
    run_high_throughput_pipeline("pdb_list.txt")
