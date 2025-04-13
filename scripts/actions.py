import re
import os

from ibookdb import getAnnotations, annotationsCount
from utils import TimeConvert, markdown_format





class Actions():
    def __init__(self):
        self.notes = self.get_annotations()
        self.notes_counter = annotationsCount()
        
    def get_annotations(self):
        notes = getAnnotations()
        for note in notes:
            modify_date = TimeConvert.get_time(float(note['modify_date']))
            note.update({'modify_date_fmt': modify_date})
        return notes

    def getBooksLists(self):
        books = {}
        for idx, val in enumerate(self.notes_counter):
            author = val['author']
            title = val['title']
            highlight_count = val['selected_text_count']
            note_count = val['note_count']
            representative_count = val['representative_text_count']

            print(f"{idx+1}. {author} -《{title}》 --> 高亮数量：{highlight_count} | 笔记数量：{note_count} | 重要标记数量：{representative_count}")
            
            books[idx+1] = title
        return books

    @markdown_format
    def getAnnotationsDetails(self, book=None) -> list:
        notes = []
        for _note in self.notes:
            if book and _note['title'] != book:
                continue
            notes.append(_note)
        return notes
    
    @markdown_format
    def search(self, target):
        # notes = self.getAnnotationsDetails()
        notes = self.notes
        search_res = []
        for note in notes:
            _ = [i for i in note.values() if i is not None and not isinstance(i, float)] # 排除时间戳和None字段
            strings = ''.join(_)
            if re.search(target, strings):
                search_res.append(note)
        
        if search_res:
            print('Found annotations!')
        else:
            print('Nothing found!')

        return search_res
    
    def write_md(self, book, notes, output):
        """
        将笔记写入 markdown 文件
        :param book: 书名
        :param notes: 笔记内容
        :param output: 输出路径
        """
        if book:
            file = os.path.join(output, f'{book}.md')
        else:
            file = os.path.join(output, 'annotations.md')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(notes)

    def export(self, book, output):
        if book:
            res = self.getAnnotationsDetails(book)
            self.write_md(book, res, output)
            print(f'Exported {book} successfully!')
        else:
            res = self.getAnnotationsDetails()
            self.write_md(None, res, output)
            print('Exported all annotations successfully!')






def main():
    pass


if __name__ == "__main__":
    main()
