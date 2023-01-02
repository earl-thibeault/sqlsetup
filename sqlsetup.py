import re

def parseschema(schema):
    mstrdict={}
    regtblnme=re.compile('CREATE TABLE IF NOT EXISTS \"(.+)\"')
    regcol=re.compile("\"([0-9,A-Z]+)\" (TEXT|INTEGER|DATE|REAL)")
    with open(schema, 'r') as f:
        txt=f.read()
    sarry=txt.split('\n')
    for e in sarry:
        e=e.strip(' ')
        tbl=re.match(regtblnme,e)
        col=re.match(regcol, e)
        if tbl:
            tbln=str(tbl.group(1))
            mstrdict[tbln]=[]
            lst=mstrdict[tbln]
        elif col:
            collumn=(col.group(1),col.group(2))
            lst.append(collumn)
    return mstrdict
def mkmodel(schema):
    m=open('models.py','w')
    imported="from sqlalchemy import Column\nfrom sqlalchemy.types import DATE, REAL, INTEGER, TEXT\nfrom .database import Base\n\n "  
    m.write(imported)
    m.close()
    tbls=schema.keys()
    for tbl in tbls:
        tblstr=f"\nclass {tbl}(Base):\n\n   __tablename__ = \"{tbl}\"\n\n"
        with open('models.py','a')  as m:
            m.write(tblstr)
        for col in schema[tbl]:
            colstr=f"   {col[0]} = Column({col[1]})\n"
            with open('models.py','a') as m:
                m.write(colstr)
             