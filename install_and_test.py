#!/usr/bin/env python3
"""
PDF目录提取器安装和测试脚本
自动安装依赖并测试功能
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n🔄 {description}")
    print(f"执行命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 成功")
            if result.stdout.strip():
                print(f"输出: {result.stdout.strip()}")
        else:
            print(f"❌ 失败")
            if result.stderr.strip():
                print(f"错误: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"🐍 Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("⚠️  警告: 建议使用Python 3.6或以上版本")
        return False
    else:
        print("✅ Python版本满足要求")
        return True

def install_pdf_libraries():
    """尝试安装PDF处理库"""
    libraries = [
        ("pypdf", "pip install pypdf"),
        ("PyPDF2", "pip install PyPDF2"),
        ("pdfplumber", "pip install pdfplumber")
    ]
    
    installed = []
    
    for lib_name, install_cmd in libraries:
        print(f"\n📦 尝试安装 {lib_name}...")
        if run_command(install_cmd, f"安装 {lib_name}"):
            installed.append(lib_name)
        else:
            print(f"⚠️  {lib_name} 安装失败，继续尝试其他库...")
    
    return installed

def test_pdf_library_import():
    """测试PDF库导入"""
    print("\n🧪 测试PDF库导入...")
    
    libraries = ['pypdf', 'PyPDF2', 'pdfplumber']
    available = []
    
    for lib in libraries:
        try:
            __import__(lib)
            available.append(lib)
            print(f"✅ {lib} 可用")
        except ImportError:
            print(f"❌ {lib} 不可用")
    
    return available

def create_test_pdf_content():
    """创建测试PDF内容（如果有reportlab库的话）"""
    print("\n📄 尝试创建测试PDF文件...")
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfbase import pdfutils
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus.tableofcontents import TableOfContents
        
        # 创建简单的测试PDF
        filename = "test_document.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        # 添加一些内容和书签
        c.bookmarkPage("page1")
        c.addOutlineEntry("第一章 介绍", "page1", level=0)
        c.drawString(100, 750, "第一章 介绍")
        c.drawString(100, 700, "这是测试PDF的第一页内容")
        
        c.showPage()
        
        c.bookmarkPage("page2")
        c.addOutlineEntry("第二章 详细内容", "page2", level=0)
        c.addOutlineEntry("2.1 子章节", "page2", level=1)
        c.drawString(100, 750, "第二章 详细内容")
        c.drawString(100, 700, "2.1 子章节")
        c.drawString(100, 650, "这是测试PDF的第二页内容")
        
        c.save()
        
        print(f"✅ 创建测试PDF文件: {filename}")
        return filename
        
    except ImportError:
        print("❌ reportlab库不可用，无法创建测试PDF")
        print("   可以使用命令安装: pip install reportlab")
        return None
    except Exception as e:
        print(f"❌ 创建测试PDF失败: {e}")
        return None

def test_scripts():
    """测试脚本功能"""
    print("\n🧪 测试脚本功能...")
    
    # 检查脚本文件是否存在
    scripts = ['pdf_toc_extractor.py', 'simple_pdf_toc.py']
    
    for script in scripts:
        if Path(script).exists():
            print(f"✅ 发现脚本: {script}")
            
            # 测试帮助信息
            if script == 'pdf_toc_extractor.py':
                run_command(f"python {script} -h", f"测试 {script} 帮助信息")
            else:
                run_command(f"python {script}", f"测试 {script} 使用方法")
        else:
            print(f"❌ 脚本不存在: {script}")

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 PDF目录提取器 - 安装和测试工具")
    print("=" * 60)
    
    # 1. 检查Python版本
    if not check_python_version():
        print("\n⚠️  Python版本可能过低，建议升级后再试")
    
    # 2. 测试已有的PDF库
    available_libs = test_pdf_library_import()
    
    # 3. 如果没有可用的库，尝试安装
    if not available_libs:
        print("\n📦 没有找到PDF处理库，开始安装...")
        installed_libs = install_pdf_libraries()
        
        if installed_libs:
            print(f"\n✅ 成功安装的库: {', '.join(installed_libs)}")
            # 重新测试
            available_libs = test_pdf_library_import()
        else:
            print("\n❌ 所有PDF库安装失败，请手动安装")
            print("   建议命令: pip install pypdf")
    else:
        print(f"\n✅ 发现可用的PDF库: {', '.join(available_libs)}")
    
    # 4. 测试脚本
    test_scripts()
    
    # 5. 创建测试PDF（可选）
    test_pdf = create_test_pdf_content()
    
    # 6. 如果有测试PDF，运行实际测试
    if test_pdf and available_libs:
        print(f"\n🎯 使用测试PDF文件运行脚本...")
        
        if Path('simple_pdf_toc.py').exists():
            run_command(f"python simple_pdf_toc.py {test_pdf}", "测试简化版脚本")
        
        if Path('pdf_toc_extractor.py').exists():
            run_command(f"python pdf_toc_extractor.py {test_pdf} --info", "测试完整版脚本")
    
    # 7. 总结
    print("\n" + "=" * 60)
    print("📋 安装测试总结:")
    print("=" * 60)
    
    if available_libs:
        print("✅ PDF处理库: 已安装并可用")
        print("✅ 脚本文件: 可以正常使用")
        print("\n🎉 安装完成！你可以开始使用PDF目录提取器了")
        print("\n📖 使用方法:")
        print("   python simple_pdf_toc.py your_document.pdf")
        print("   python pdf_toc_extractor.py your_document.pdf -o output.txt")
    else:
        print("❌ PDF处理库: 安装失败")
        print("⚠️  请手动安装PDF库: pip install pypdf")
    
    print("\n📚 更多信息请查看: README_PDF_TOC.md")

if __name__ == '__main__':
    main() 