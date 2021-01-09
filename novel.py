from bs4 import BeautifulSoup
import requests
import urllib
import time
import os

'''
なろう小説のテキストファイルを生成
・保存するファイル名をnovel_titleに設定する
・ノベルのページのURLをnovel_urlに設定する
連番でURLを探索するのでページが見つからない場合に自動で停止する

例：
novel_title = "乙女ゲームの破滅フラグしかない悪役令嬢に転生してしまった"
novel_url = "https://ncode.syosetu.com/n4830bu/"
'''

#保存時のファイルタイトル
novel_title = "honnsukino"

#取得ページURL
novel_url = "https://ncode.syosetu.com/n4830bu/"

file_path = os.path.dirname(__file__)
save_path = file_path + novel_title + ".txt"

num_table = str.maketrans('1234567890','１２３４５６７８９０')

#初期ページナンバー
page_number = 1

def addHeading(letNum, title):
  num_str = str(letNum)
  txt = '［＃{letNum}字下げ］{title}［＃「{title}」は中見出し］'.format(letNum=num_str.translate(num_table), title=title )
  return "\n\n" + txt +"\n\n"

with open(save_path, mode='w') as f:
    while True:
        all_txt = []
        try:
            url = novel_url+str(page_number)
            html = urllib.request.urlopen(url)
            soup = BeautifulSoup(html, "html.parser")

        except OSError as e:
          print("html not found \n  scraping finished")
          break

        except Exception as e:
          print(e)
          break

        #タイトルナンバー
        #title_no_html = soup.find("div", id="novel_no")
        #title_no = title_no_html.string + "\n"
        #all_txt.append(title_no)

        #タイトル抽出
        title_html = soup.find("p", class_="novel_subtitle")
        #title = title_html.string + "\n"      
        title = addHeading(1, title_html.string)
        all_txt.append(title)

        #本文抽出
        honbun = soup.find("div", id="novel_honbun").find_all("p")
        for txt in honbun:
          if txt.string == None:
            all_txt.append("\n")
          else:
            all_txt.append(txt.string)
        
        #本文結合
        data_txt = ''.join(all_txt)

        #本文ファイル書き込み
        f.write(data_txt)

        #進行ログ
        print('{}:ページ'.format(page_number))

        #次ページナンバー
        page_number +=1 

        #処理遅延(web負荷低減)
        time.sleep(0.5)