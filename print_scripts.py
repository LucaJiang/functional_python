from bs4 import BeautifulSoup
import re


def extract_notes_from_html(filepath):
    """
    从 reveal.js 的 HTML 文件中提取演讲者备注。

    - 跳过 data-visibility="hidden" 的 section。
    - 提取每个 section 的 h2 或 h3 标题。
    - 提取 <aside class="notes"> 中的文本。
    - 清理文本中的换行符和多余空格。
    - 将结果打印出来。
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {filepath}")
        return

    soup = BeautifulSoup(html_content, "lxml")
    sections = soup.find_all("section")

    all_notes = []

    for section in sections:
        # 如果 section 是隐藏的，则跳过
        if section.get("data-visibility") == "hidden":
            continue

        # 查找 h2 或 h3 标题
        heading_tag = section.find(["h2", "h3"])
        if heading_tag:
            # 清理标题文本，移除换行符
            heading_text = " ".join(heading_tag.get_text(strip=True).split())
        else:
            heading_text = "无标题"

        # 查找备注
        notes_tag = section.find("aside", class_="notes")
        if notes_tag:
            # 获取备注文本，并用空格替换所有空白字符（包括换行符）
            notes_text = " ".join(notes_tag.get_text(strip=True).split())

            # 组合标题和备注
            all_notes.append(f"{notes_text}\n")
            # all_notes.append(f"### {heading_text}\n\n{notes_text}\n")

    return "\n".join(all_notes)


if __name__ == "__main__":
    # 将 'index.html' 替换为你的文件路径
    notes_script = extract_notes_from_html("index.html")
    if notes_script:
        print(notes_script)
        # 如果想保存到文件，可以使用以下代码
        with open("notes.md", "w", encoding="utf-8") as f:
            f.write(notes_script)
        print("备注已保存到 notes.md")
