import sqlite3
import functools
from typing import (List, Dict, Union)

from utils import EnvPath

SqlResultType = List[Dict[str, Union[str, int]]]

ANNOTATION_DB_FILES = list(EnvPath.ANNOTATION_DB_DIR.glob('*.sqlite'))
BOOKS_DB_FILES = list(EnvPath.BOOKS_DB_DIR.glob('*.sqlite'))

ATTACH_BOOKS_SQL =  """
attach database ? as books
"""

GET_DATA_SQL = """
select a.zauthor as author
    ,a.ztitle as title
    ,b.ZFUTUREPROOFING5 as chapter
    ,b.ZANNOTATIONSELECTEDTEXT as selected_text
    ,b.ZANNOTATIONNOTE as note
    ,b.ZANNOTATIONREPRESENTATIVETEXT as representative_text
    ,b.ZANNOTATIONMODIFICATIONDATE as modify_date
from
(
select ZASSETID
	,ZAUTHOR
	,ztitle
from books.ZBKLIBRARYASSET
) a
right join
(
select ZFUTUREPROOFING5
	,ZANNOTATIONNOTE
	,ZANNOTATIONSELECTEDTEXT
	,ZANNOTATIONREPRESENTATIVETEXT
	,ZANNOTATIONASSETID
	,ZANNOTATIONMODIFICATIONDATE
from ZAEANNOTATION
where ZANNOTATIONSELECTEDTEXT is not null
group by ZFUTUREPROOFING5
	,ZANNOTATIONSELECTEDTEXT
	,ZANNOTATIONASSETID
	,ZANNOTATIONMODIFICATIONDATE
) b
on a.ZASSETID=b.ZANNOTATIONASSETID
"""

DATA_FIELDS = [
    'author',
    'title',
    'chapter',
    'selected_text',
    'note',
    'representative_text',
    'modify_date'
]



@functools.lru_cache(maxsize=1)
def attachDB():
    if len(BOOKS_DB_FILES) == 0:
        raise FileNotFoundError("Books database not found")
    else:
        books_db_file = BOOKS_DB_FILES[0]

    if len(ANNOTATION_DB_FILES) == 0:
        raise FileNotFoundError("Annotation database not found")
    else:
        annotation_db_file = ANNOTATION_DB_FILES[0]

    conn_books_db = sqlite3.connect(str(annotation_db_file), check_same_thread=False)
    cursor = conn_books_db.cursor()
    cursor.execute(ATTACH_BOOKS_SQL, (str(books_db_file),))
    return cursor
        

def getAnnotations() -> SqlResultType:
    cursor = attachDB()
    execute = cursor.execute(GET_DATA_SQL)
    res = execute.fetchall()
    annotations = [dict(zip(DATA_FIELDS, row)) for row in res]
    return annotations



DATA_COUNT_SQL = """
select a.zauthor as author
    ,a.ztitle as title
    ,count(b.ZANNOTATIONSELECTEDTEXT) as selected_text_count
    ,count(b.ZANNOTATIONNOTE) as note_count
    ,count(b.ZANNOTATIONREPRESENTATIVETEXT) as representative_text_count
from
(
select ZASSETID
	,ZAUTHOR
	,ztitle
from books.ZBKLIBRARYASSET
) a
right join
(
select 
	 ZANNOTATIONNOTE
	,ZANNOTATIONSELECTEDTEXT
	,ZANNOTATIONREPRESENTATIVETEXT
	,ZANNOTATIONASSETID
from ZAEANNOTATION
where ZANNOTATIONSELECTEDTEXT is not null
group by 
	 ZANNOTATIONSELECTEDTEXT
	,ZANNOTATIONASSETID
) b
on a.ZASSETID=b.ZANNOTATIONASSETID
group by a.zauthor
    ,a.ztitle
"""

COUNT_FIELDS = [
    'author',
    'title',
    'selected_text_count',
    'note_count',
    'representative_text_count'
]




def annotationsCount() -> SqlResultType:
    cursor = attachDB()
    execute = cursor.execute(DATA_COUNT_SQL)
    res = execute.fetchall()
    annotations = [dict(zip(COUNT_FIELDS, row)) for row in res]
    return annotations



def main():
    annotations = getAnnotations()
    count = annotationsCount()
    print(annotations)


if __name__ == "__main__":
    main()
            
