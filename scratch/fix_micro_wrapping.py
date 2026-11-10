with open('scratch/build_right_tabbed_workbench.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('ORIGIN · 起运港 (POL)', 'POL · 起运港')
code = code.replace('DEST · 目的港 (POD)', 'POD · 目的港')
code = code.replace('''      const getPortCnName = (code) => {
        const map = {
          CNTAO: '青岛港 · QINGDAO',
          CNSHA: '上海港 · SHANGHAI',
          USLAX: '洛杉矶港 · LA',
          USLGB: '长滩港 · LB'
        };
        return map[code] || code || '未指定港口';
      };''', '''      const getPortCnName = (code) => {
        const map = {
          CNTAO: '青岛港',
          CNSHA: '上海港',
          USLAX: '洛杉矶港',
          USLGB: '长滩港'
        };
        return map[code] || code || '未指定港口';
      };''')

with open('scratch/build_right_tabbed_workbench.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated POL/POD labels for full center pill visibility.")
