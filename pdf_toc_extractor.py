#!/usr/bin/env python3
"""
PDF目录结构提取器
提取PDF文件的目录(TOC/书签)并以树状格式显示和导出
"""

import argparse
import sys
from pathlib import Path
import re

try:
    import pypdf
except ImportError:
    print("错误: 需要安装pypdf库")
    print("请运行: pip install pypdf")
    sys.exit(1)

def clean_title(title):
    """清理目录标题，移除特殊字符"""
    if not title:
        return "未命名"
    
    # 移除或替换特殊字符
    cleaned = re.sub(r'[\r\n\t]', ' ', title)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.strip()
    
    return cleaned if cleaned else "未命名"

def extract_bookmarks(pdf_reader):
    """提取PDF书签/目录结构"""
    try:
        outlines = pdf_reader.outline
        if not outlines:
            return []
        return parse_outline_tree(outlines)
    except Exception as e:
        print(f"提取书签时出错: {e}")
        return []

def parse_outline_tree(outlines, level=0):
    """递归解析目录树结构"""
    tree = []
    
    i = 0
    while i < len(outlines):
        item = outlines[i]
        
        if isinstance(item, list):
            # 嵌套的子目录列表
            if tree:  # 如果有父级项目，将这些子项添加为children
                tree[-1]['children'].extend(parse_outline_tree(item, level + 1))
            else:  # 如果没有父级，直接添加到当前级别
                tree.extend(parse_outline_tree(item, level))
        else:
            # 单个书签项
            try:
                title = clean_title(item.title)
                page = None
                
                # 尝试获取页码
                if hasattr(item, 'page') and item.page:
                    try:
                        if hasattr(item.page, 'idnum'):
                            page = item.page.idnum
                        else:
                            page = str(item.page)
                    except:
                        page = None
                
                bookmark_info = {
                    'title': title,
                    'level': level,
                    'page': page,
                    'children': []
                }
                
                tree.append(bookmark_info)
                
                # 检查下一个项目是否是子项列表
                if i + 1 < len(outlines) and isinstance(outlines[i + 1], list):
                    # 下一个项目是子项列表，递归处理并添加为当前项的children
                    bookmark_info['children'] = parse_outline_tree(outlines[i + 1], level + 1)
                    i += 1  # 跳过下一个列表项，因为已经处理了
                
            except Exception as e:
                print(f"处理书签项时出错: {e}")
        
        i += 1
    
    return tree

def format_tree_text(bookmarks, show_pages=False, indent="  "):
    """将目录树格式化为文本"""
    if not bookmarks:
        return "未找到目录结构"
    
    lines = []
    
    def format_bookmark(bookmark, current_indent="", is_last=False, parent_prefix=""):
        title = bookmark['title']
        page_info = f" (页码: {bookmark['page']})" if show_pages and bookmark['page'] else ""
        
        # 根据是否是最后一个项目选择合适的符号
        if current_indent == "":
            # 顶级项目
            prefix = "├─ "
            next_prefix = parent_prefix + "│  "
        else:
            if is_last:
                prefix = current_indent + "└─ "
                next_prefix = current_indent + "   "
            else:
                prefix = current_indent + "├─ "
                next_prefix = current_indent + "│  "
        
        lines.append(f"{prefix}{title}{page_info}")
        
        # 递归处理子项
        children = bookmark.get('children', [])
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            format_bookmark(child, next_prefix, is_last_child, next_prefix)
    
    for i, bookmark in enumerate(bookmarks):
        is_last = (i == len(bookmarks) - 1)
        format_bookmark(bookmark, "", is_last)
    
    return "\n".join(lines)

def format_tree_markdown(bookmarks, show_pages=False, base_level=1):
    """将目录树格式化为Markdown"""
    if not bookmarks:
        return "未找到目录结构"
    
    lines = []
    
    def format_bookmark(bookmark, level):
        title = bookmark['title']
        page_info = f" (页码: {bookmark['page']})" if show_pages and bookmark['page'] else ""
        
        # 使用Markdown标题格式，基于书签实际的level属性
        actual_level = bookmark.get('level', level)
        header = "#" * min(actual_level + base_level, 6)  # 最多6级标题
        lines.append(f"{header} {title}{page_info}")
        
        # 递归处理子项
        for child in bookmark.get('children', []):
            format_bookmark(child, level + 1)
    
    for bookmark in bookmarks:
        format_bookmark(bookmark, 0)
    
    return "\n".join(lines)

def extract_pdf_info(pdf_path):
    """提取PDF基本信息"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            
            info = {
                'title': None,
                'author': None,
                'pages': len(pdf_reader.pages),
                'bookmarks': []
            }
            
            # 提取元数据
            if pdf_reader.metadata:
                info['title'] = pdf_reader.metadata.get('/Title', '').strip()
                info['author'] = pdf_reader.metadata.get('/Author', '').strip()
            
            # 提取书签
            info['bookmarks'] = extract_bookmarks(pdf_reader)
            
            return info
            
    except Exception as e:
        print(f"读取PDF文件时出错: {e}")
        return None

def save_to_file(content, output_path, encoding='utf-8'):
    """保存内容到文件"""
    try:
        with open(output_path, 'w', encoding=encoding) as f:
            f.write(content)
        print(f"✓ 目录结构已保存到: {output_path}")
        return True
    except Exception as e:
        print(f"保存文件时出错: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='提取PDF文件的目录结构树',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python pdf_toc_extractor.py document.pdf                    # 在控制台显示目录
  python pdf_toc_extractor.py document.pdf -o toc.txt         # 保存为文本文件
  python pdf_toc_extractor.py document.pdf -o toc.md -f md    # 保存为Markdown
  python pdf_toc_extractor.py document.pdf --info             # 显示PDF基本信息
  python pdf_toc_extractor.py document.pdf --show-pages       # 显示页码信息
        """
    )
    
    parser.add_argument('pdf_file', help='PDF文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-f', '--format', choices=['text', 'md'], default='text',
                       help='输出格式 (text: 纯文本, md: Markdown)')
    parser.add_argument('--info', action='store_true',
                       help='显示PDF基本信息')
    parser.add_argument('--encoding', default='utf-8',
                       help='输出文件编码 (默认: utf-8)')
    parser.add_argument('--show-pages', action='store_true',
                       help='显示页码信息')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"错误: 文件不存在 - {pdf_path}")
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"警告: 文件可能不是PDF格式 - {pdf_path}")
    
    print(f"正在处理PDF文件: {pdf_path}")
    
    # 提取PDF信息
    pdf_info = extract_pdf_info(pdf_path)
    if not pdf_info:
        print("无法读取PDF文件")
        sys.exit(1)
    
    # 显示基本信息
    if args.info:
        print(f"\n📄 PDF信息:")
        print(f"   标题: {pdf_info['title'] or '无'}")
        print(f"   作者: {pdf_info['author'] or '无'}")
        print(f"   页数: {pdf_info['pages']}")
        print(f"   书签数量: {len(pdf_info['bookmarks'])}")
    
    # 格式化目录结构
    if not pdf_info['bookmarks']:
        print("\n⚠️  该PDF文件没有目录结构/书签")
        return
    
    print(f"\n📋 找到 {len(pdf_info['bookmarks'])} 个目录项")
    
    if args.format == 'md':
        content = format_tree_markdown(pdf_info['bookmarks'], show_pages=args.show_pages)
    else:
        content = format_tree_text(pdf_info['bookmarks'], show_pages=args.show_pages)
    
    # 输出结果
    if args.output:
        # 保存到文件
        output_path = Path(args.output)
        if save_to_file(content, output_path, args.encoding):
            print(f"文件大小: {output_path.stat().st_size} 字节")
    else:
        # 在控制台显示
        print("\n" + "="*50)
        print("PDF目录结构:")
        print("="*50)
        print(content)

if __name__ == '__main__':
    main() 