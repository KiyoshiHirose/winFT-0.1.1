# winFT-0.1.1
I'm pleased to announce that winFT-0.1.1 is now available for fasttext fan users or those who interested in Natural Language Processing.
winFT is developed for Facebook [fastText](https://fasttext.cc/) users who would like to use GUI on the Windows PC.
winFT support the following seven fasttext functions: Supervised, Skipgram, CBOW, Test-Label, Predict-Prob, Nearest Neighbors, and Analogies.

The following pictures are winFT main window and result of Skipgram. It's easy and intuitive operation!

winFT runs on Japanese and English Windows.

Please be advised that winFT might be modified without notice for a while.

![winFT](https://user-images.githubusercontent.com/46741075/69804504-12b10300-1222-11ea-95f6-899d9364e829.png)
![skipgram-result](https://user-images.githubusercontent.com/46741075/69804679-73d8d680-1222-11ea-8323-339a25d4642c.png)
# Software Requirements
* Windows 10
* C++ for Windows
* Python 3.6.8 or newer for Windows
* Config parser, Numpy, Pillow, WMI import modules
* git 2.24.0 for Windows
* fasttext Python API modules
* MeCab for Windows (MeCab is morphological analysis tool for Japanese)
# Hardware Requirements
* CPU : Intel CORE i7 8th Gen or newer
* MEM : Minimum 8GB is recommended
* Storage : Large enough for machine/deep learning
# Installation
* C++ for Windows

  Install Visual Studio 2019 Community version.
  
  Japanese users: install from [here](https://docs.microsoft.com/ja-jp/visualstudio/install/install-visual-studio?view=vs-2019)
  
  Non-Japanese users: install from [here](https://docs.microsoft.com/en-us/visualstudio/install/install-visual-studio?view=vs-2019)
* Python 3.6 for Windows

  Go to [Python.org for Windows](https://www.python.org/downloads/windows/) and select your favorite version. "Wdindows x86-64 executable installer" is recommended. winFT is developed under the [Python-3.6.8-amd64.exe](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe).
* Config parser, Numpy, Pillow, WMI import modules
```
pip from CMD or Power Shell window

python -V
python -m pip install --upgrade pip
pip install configparser, numpy, pillow, wmi
```
* git 2.24.0 for Windows

  Install from [here](https://git-scm.com/downloads) and select Windows. Installation exe module is downloaded automatically and execute exe module.
* fasttext Python API modules
```
git clone https://github.com/facebookresearch/fastText.git
cd fastText
pip install .
```
* winFT
```
git clone https://github.com/KiyoshiHirose/winFT-0.1.1.git

Please refer "Usage" how to run winFT.
```
* MeCab for Windows (Note: Japanese users only)

  MeCab installation is described in Japanese.
  
  Windows版mecabの日本語辞書文字コードはShift-JISコードですが、Pythonは文字コードをすべてUTF-8で処理をしていますので、mecabコマンドではShift-JISコード、fasttextAPIからはUTF-8コードの日本語辞書を用意する必要があります。2種類の文字コードの日本語辞書を作成するためには、2回インストールを行います。以下にインストレーション方法を示します。
```
はじめにpipします
pip install mecab-python-windows
```
  次にコマンド用のmecabを[ここから](https://github.com/ikegami-yukino/mecab/releases)mecab-64-0.996.2.exeをインストールします。
  
  1回目はデフォルトのSHIFT-JISコードで、CまたはD:\MeCab にインストールします。インストール後、C:\MeCab\dic\ipadic → C:\MeCab\dic\ipadic-sjis にディレクトリ名を変更します。
  
  2回目はUTF-8コードで、CまたはD:\MeCab にインストールします。インストール後、C:\MeCab\dic\ipadic → C:\MeCab\dic\ipadic-utf8 にディレクトリ名を変更します。
  
  次にC:\MeCab\etc\mecabrcを修正します。
  
  dicdir =  $(rcpath)\..\dic\ipadic → dicdir =  $(rcpath)\..\dic\ipadic-sjis
  
  このままではfasttextAPI使用時に文字化けを起こしますので、config.ini の[mecab]タブに ini_cab_dir = -d c:/mecab/dic/ipadic-utf8を指定します。
* Usage
  1. Launch file explore
  2. Locate winFT installation folder
  3. Right click winfasttext.pyw
  4. Send to Desktop as shortcut
  5. Open propaties of shortcut and insert "pythonw " into link textbox, then apply or exit
  6. Double click shortcut, the above winFT window will appear on your screen
* Examples

  Predict-Prob.
  
  This is an example of polarity(Positive/Even/Negative expressions) analysis. Polarity corpus is developed by author.
  ![predict-prob](https://user-images.githubusercontent.com/46741075/69818114-70077d00-123f-11ea-85b2-fc8d7231495a.png)
  ![predict-result](https://user-images.githubusercontent.com/46741075/69818175-87df0100-123f-11ea-95ce-d176d69d22fa.png)
  
  
  Nearest Neighbors.
  
  This is an example of text8, fanous corpus of Word2Vec.
  ![nn](https://user-images.githubusercontent.com/46741075/69818324-db514f00-123f-11ea-8dc3-be98d71acb61.png)
  ![nn-result](https://user-images.githubusercontent.com/46741075/69818355-edcb8880-123f-11ea-80b3-a1d345944000.png)

  Analogies.
  
  This is an example of text8, famous corpus of Word2Vec. 
  ![analogies](https://user-images.githubusercontent.com/46741075/69818460-24090800-1240-11ea-87fc-4dcb54438674.png)
  ![analogies-result](https://user-images.githubusercontent.com/46741075/69818485-308d6080-1240-11ea-98b6-7fc36a405c5c.png)

* Note

  Please use UTF-8 character code when you create a corpus. Keep in mind everything is UTF-8.
  
  winFT accepts both carriage return, \<CR\>\<LF\> and \<LF\>.
* Author

  Kiyoshi Hirose, Representative of HIT Business Consulting Firm (Self employed).
  
  Focusing both business and technical strategies for AI implementation.

  Certificate "Artificial Intelligence: Implications for Business Strategy" from MIT Sloan school of management.
* License

  MIT License.
