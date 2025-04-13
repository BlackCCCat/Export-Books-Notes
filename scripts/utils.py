import pathlib
import functools

from datetime import datetime


class EnvPath():
    HOME_DIR = pathlib.Path.home()

    ANNOTATION_DB_DIR = HOME_DIR / 'Library/Containers/com.apple.iBooksX/data/Documents/AEAnnotation'
    BOOKS_DB_DIR = HOME_DIR / 'Library/Containers/com.apple.iBooksX/data/Documents/BKLibrary'

    EXPORT_DIR = './books'


    @staticmethod
    def set_export_dir(dir :str):
        EnvPath.EXPORT_DIR = dir



class TimeConvert():
    BASE_TIMESTAMP = 978307200
    @staticmethod
    def get_time(ts :float) -> str:
        _time = datetime.fromtimestamp(ts + TimeConvert.BASE_TIMESTAMP)
        return _time.strftime('%Y-%m-%d %H:%M:%S')
    

def markdown_format(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        # 字典来存储按 title 和 chapter 分类的文本
        formatted_output = {}
        
        for item in result:
            title = item['title']
            chapter = item['chapter']
            selected_text = item['selected_text']
            author = item['author']
            modify_date = item['modify_date_fmt']
            note = item['note'] if item['note'] else '无'

            # 创建 markdown 结构
            if title not in formatted_output:
                formatted_output[title] = {}

            if chapter not in formatted_output[title]:
                formatted_output[title][chapter] = []

            formatted_output[title][chapter].append({
                'author': author,
                'modify_date': modify_date,
                'selected_text': selected_text,
                'note': note
            })

        # 转为 markdown 字符串
        markdown_result = []
        for title, chapters in formatted_output.items():
            markdown_result.append(f"# 《{title}》")
            markdown_result.append(f"作者：{chapters[list(chapters.keys())[0]][0]['author']}")
            for chapter, details in chapters.items():
                markdown_result.append(f"## {chapter}")
                for detail in details:
                    markdown_result.append(f"> 修改时间：{detail['modify_date']}")
                    markdown_result.append(f"- {detail['selected_text']}")
                    markdown_result.append("### 笔记")
                    markdown_result.append(detail['note'])
        
        return "\n".join(markdown_result)
    
    return wrapper

def main():
    print(EnvPath.EXPORT_DIR)
    EnvPath.set_export_dir(f'{EnvPath.HOME_DIR}/Desktop')
    print(EnvPath.EXPORT_DIR)

    ts = datetime.now().timestamp()
    print(ts)
    print(TimeConvert.get_time(ts))


if __name__ == "__main__":
    main()