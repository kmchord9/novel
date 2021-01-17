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
novel_title = "無職転生"

#取得ページURL
narou_url = "https://ncode.syosetu.com"
novel_url =  "/n9669bk/"

file_path = os.path.dirname(__file__)
save_path = file_path + novel_title + ".txt"

num_table = str.maketrans('1234567890','１２３４５６７８９０')

#初期ページナンバー
page_number = 1

#本文とタイトル要素
novel_html = urllib.request.urlopen(narou_url + novel_url)
novel_soup = BeautifulSoup(novel_html, "html.parser")
link_els = novel_soup.find("div", class_="index_box").find_all(class_=["chapter_title", "novel_sublist2"])

def addHeading(letNum, title):
  num_str = str(letNum)
  txt = '［＃{letNum}字下げ］{title}［＃「{title}」は中見出し］'.format(letNum=num_str.translate(num_table), title=title )
  return "\n\n" + txt +"\n\n"

def createSavePath(addName):
  return file_path + novel_title + addName + ".txt"


with open(save_path, mode='w') as f:

  for link_el in link_els:
    all_txt = []
    try:
      #hrefのリンク取得
      link_url = narou_url + link_el.a.get('href')

      #本文ページのsoupオブジェクト作成
      html = urllib.request.urlopen(link_url)
      soup = BeautifulSoup(html, "html.parser")

      #タイトル抽出
      title_html = soup.find("p", class_="novel_subtitle")
      title = addHeading(3, title_html.string)
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

    except AttributeError as e:
      #ファイルを開いていたら閉じる
      #try:
      #  f.close()
      #except NameError as e:
      #  pass

      #f = open(createSavePath(''.join(link_el.string.split())), mode='w',encoding='utf-8')

      #章タイトル

      syoutitle = addHeading(5, ''.join(link_el.string.split()))
      f.write(syoutitle)   

    except Exception as e:
      print(e)
      break 
