# PDF 目录结构提取器

这个工具包提供了Python脚本来提取PDF文件的目录结构（书签/大纲）并以树状格式导出。

## 文件说明

### 1. `pdf_toc_extractor.py` - 主要功能脚本
- 功能最全面的版本
- 支持多种输出格式（文本、Markdown）
- 提供命令行参数和详细帮助
- 支持页码提取和PDF元数据显示
- 递归解析嵌套目录结构

### 2. `install_and_test.py` - 安装和测试工具
- 自动检测和安装PDF处理库
- 测试脚本功能
- 创建测试PDF文件
- 提供安装诊断和故障排除

### 3. `example_output/` - 示例输出目录
- `toc.txt` - 文本格式输出示例
- `toc.md` - Markdown格式输出示例

## 快速开始

### 1. 安装依赖（推荐使用自动安装脚本）
```bash
python install_and_test.py
```

### 2. 手动安装依赖
推荐按以下顺序尝试：

#### 方法1：安装pypdf（推荐）
```bash
pip install pypdf
```

#### 方法2：安装PyPDF2
```bash
pip install PyPDF2
```

#### 方法3：安装pdfplumber（功能更强）
```bash
pip install pdfplumber
```

## 使用方法

### 基本用法
```bash
# 在控制台显示目录结构
python pdf_toc_extractor.py document.pdf

# 显示PDF基本信息
python pdf_toc_extractor.py document.pdf --info

# 显示页码信息
python pdf_toc_extractor.py document.pdf --pages
```

### 保存到文件
```bash
# 保存为文本文件（默认格式）
python pdf_toc_extractor.py document.pdf -o toc.txt

# 保存为Markdown格式
python pdf_toc_extractor.py document.pdf -o toc.md --format markdown

# 同时显示页码信息
python pdf_toc_extractor.py document.pdf -o toc.txt --pages
```

### 高级参数
```bash
# 指定输出编码
python pdf_toc_extractor.py document.pdf -o toc.txt --encoding gbk

# 查看完整帮助
python pdf_toc_extractor.py --help
```

## 输出格式示例

### 文本格式（树状结构）
```
├─ Contents
├─ Acknowledgements
├─ Changes from Previous Versions
│  ├─ Jan 1, 2025 - This Version
│  ├─ Dec 4, 2023
│  ├─ March 15, 2022
│  └─ December, 12, 2020
├─ Introduction
│  ├─ Why This Book Exists
│  │  ├─ What is Sustainability?
│  │  ├─ Why Care About Sustainability?
│  │  └─ How to Value Sustainability
│  └─ The Rails Application Architecture
└─ Deep Dive into Rails
```

### Markdown格式
```markdown
# PDF目录结构

# Contents

# Acknowledgements

# Changes from Previous Versions

## Jan 1, 2025 - This Version

## Dec 4, 2023

## March 15, 2022

## December, 12, 2020

# Introduction

## Why This Book Exists

### What is Sustainability?

### Why Care About Sustainability?
```

### 带页码信息的输出
```
├─ Contents (页码: 3)
├─ Introduction (页码: 15)
│  ├─ Why This Book Exists (页码: 16)
│  └─ What is Sustainability? (页码: 18)
```

## 特色功能

- ✅ **智能目录解析**：递归解析复杂的嵌套目录结构
- ✅ **多种输出格式**：支持文本树状格式和Markdown格式
- ✅ **页码提取**：自动提取并显示章节页码
- ✅ **PDF元数据**：显示标题、作者、页数等信息
- ✅ **编码支持**：支持UTF-8和其他编码格式
- ✅ **错误处理**：友好的错误提示和故障排除
- ✅ **自动安装**：包含自动依赖安装和测试脚本

## 注意事项

1. **PDF兼容性**：并非所有PDF文件都包含书签/目录信息
2. **中文支持**：完全支持中文PDF文件和目录
3. **大文件处理**：对于大型PDF文件，提取过程可能需要一些时间
4. **权限问题**：某些受保护的PDF文件可能无法读取
5. **目录层级**：支持无限嵌套的目录层级结构

## 故障排除

### 常见问题

1. **ImportError: 需要安装pypdf库**
   ```bash
   # 运行自动安装脚本
   python install_and_test.py
   
   # 或手动安装
   pip install pypdf
   ```

2. **无法读取PDF文件**
   ```
   可能原因：
   - 文件损坏或受保护
   - 文件路径不正确
   - 权限不足
   - PDF文件没有嵌入目录信息
   ```

3. **没有目录结构**
   ```
   说明：该PDF文件没有书签/大纲信息
   脚本会显示"未找到目录结构"的提示
   ```

4. **中文显示乱码**
   ```bash
   # 解决方案：指定编码格式
   python pdf_toc_extractor.py document.pdf -o toc.txt --encoding utf-8
   ```

### 诊断工具

使用内置的诊断脚本检查环境：
```bash
python install_and_test.py
```

该脚本会自动：
- 检查Python版本
- 测试PDF库可用性
- 安装缺失的依赖
- 创建测试PDF并验证功能

## 支持的PDF库对比

| 库名 | 安装命令 | 特点 |
|------|----------|------|
| pypdf | `pip install pypdf` | 新版本，活跃维护，推荐使用 |
| PyPDF2 | `pip install PyPDF2` | 经典库，兼容性好 |
| pdfplumber | `pip install pdfplumber` | 功能强大，支持表格提取 |

## 使用示例

### 批量处理多个PDF文件
```bash
# 使用shell循环处理多个文件
for file in *.pdf; do
    python pdf_toc_extractor.py "$file" -o "${file%.pdf}_toc.txt"
done
```

### 生成网页友好的输出
```bash
# 生成Markdown格式，可直接用于文档网站
python pdf_toc_extractor.py document.pdf -o toc.md --format markdown
```

## 示例文件类型

以下类型的PDF文件通常包含良好的目录结构：
- 📚 技术书籍和教程
- 📄 学术论文和研究报告
- 📖 官方手册和用户指南
- 💼 企业报告和白皮书
- 📋 政府文档和标准规范

## 扩展和定制

项目采用模块化设计，易于扩展：
- 添加新的输出格式
- 集成到其他工具或工作流
- 自定义目录解析逻辑
- 批量处理功能

## 项目结构

```
pdf_toc_extractor/
├── pdf_toc_extractor.py    # 主要功能脚本
├── install_and_test.py     # 安装和测试工具
├── example_output/         # 示例输出文件
│   ├── toc.txt            # 文本格式示例
│   └── toc.md             # Markdown格式示例
├── README.md              # 项目文档
└── .gitignore            # Git忽略文件配置
```
