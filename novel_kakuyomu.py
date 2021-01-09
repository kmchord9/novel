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
novel_title = "zennkoutei"

#取得ページURL
novel_url = "https://kakuyomu.jp/works/1177354054886505887"

file_path = os.path.dirname(__file__)
save_path = file_path + novel_title + ".txt"

num_table = str.maketrans('1234567890','１２３４５６７８９０')

#初期ページナンバー
page_number = 1

#本文リンク抽出
novel_html = urllib.request.urlopen(novel_url)
novel_soup = BeautifulSoup(novel_html, "html.parser")
link = novel_soup.find("ol", class_="widget-toc-items test-toc-items").find_all("a")
link_lists = [data.get('href') for data in link]


def addHeading(letNum, title):
  num_str = str(letNum)
  txt = '［＃{letNum}字下げ］{title}［＃「{title}」は中見出し］'.format(letNum=num_str.translate(num_table), title=title )
  return "\n\n" + txt +"\n\n"

with open(save_path, mode='w') as f:

  for link_list in link_lists:
    all_txt = []
    html = urllib.request.urlopen("https://kakuyomu.jp"+link_list)
    soup = BeautifulSoup(html, "html.parser")

    #章確認
    chapter_html = soup.find("p", class_="chapterTitle level1 js-vertical-composition-item")

    try:
      chapter_no = chapter_html.string
      all_txt.append(addHeading(5,chapter_no))

    except AttributeError as e:
      pass

    except Exception as e:
      print(e)
      break

    #タイトル
    title_html = soup.find("p", class_="widget-episodeTitle js-vertical-composition-item")
    title = addHeading(2, title_html.string)
    all_txt.append(title)

    #本文
    honbun = soup.find("div", class_="widget-episodeBody js-episode-body").find_all("p")
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