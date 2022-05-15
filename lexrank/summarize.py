import sys
import re

import getopt

from pprint import pprint

# https://ohke.hateblo.jp/entry/2018/11/17/230000


from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenizer import Tokenizer as JanomeTokenizer  # sumyのTokenizerと名前が被るため
from janome.tokenfilter import POSKeepFilter, ExtractAttributeFilter

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def main():
	ret = 0

	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"hvo:c:d",
			[
				"help",
				"version",
				"output=",
				"sentences-count=",
				"debug"
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)
	
	output = None
	sentences_count = 2
	debug = False
	
	for o, a in opts:
		if o == "-v":
			usage()
			sys.exit(0)
		elif o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-o", "--output"):
			output = a
		elif o in ("-debug", "--debug"):
			debug = True
		elif o in ("-c", "--sentences-count"):
			sentences_count = int(a)
	
	if ret != 0:
		sys.exit(1)
	
	if output is not None :
		fp_out = open(output, mode='w', encoding='utf-8')
	else :
		fp_out = sys.stdout
	

	for filepath in args:
		count = 1
	
		fp = open(filepath, mode='r', encoding='utf-8')
		while True :
			if debug :
				print("INFO : count {0}".format(count))
			
			count += 1
			line = fp.readline()
			if not line:
				break
			
			line = line.rstrip()
			line = line.lstrip()
			
			if re.search(r'^\s*$', line) :
				continue
			
			if debug :
				print('LINE : {0}'.format(line))
			
			sentences = []
			#sentences = re.split(r'[^」]。', line)
			while True :
				m = re.search(r'^(「.+?」|[^「」]+?。)(.*)', line)
				if m :
					token = m.groups(1)[0]
					newline = m.groups(1)[1]
					
					#print('TOKEN : {0}'.format(token))
					sentences.append(token)
					line = newline
				else :
					break
				
				#print('NEWLINE : {0}'.format(newline))
			
			if debug :
				for i in range(len(sentences)) :
					print('  SENTENCES[{0}] : {1}'.format(i, sentences[i]))

			# ()「」、。は全てスペースに置き換える
			char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)「」、。]', ' ')]
			tokenizer	= JanomeTokenizer()

			# 名詞・形容詞・副詞・動詞の原型のみ
			token_filters = [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')]

			# 形態素解析器を作る
			analyzer = Analyzer(
				char_filters=char_filters,
				tokenizer=tokenizer,
				token_filters=token_filters,
			)
			
			#pprint(sentences)

			# 抽出された単語をスペースで連結
			# 末尾の'。'は、この後使うtinysegmenterで文として分離させるため。
			corpus = [' '.join(analyzer.analyze(s)) + '。' for s in sentences]
			#for i in range(2):
			#
			#	print(corpus[i])
			if debug :
				for i in range(len(corpus)) :
					print('  CORPUS[{0}] : {1}'.format(i, corpus[i]))

			# 連結したcorpusを再度tinysegmenterでトークナイズさせる
			parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))

			# LexRankで要約を2文抽出
			summarizer = LexRankSummarizer()
			summarizer.stop_words = [' ']  # スペースも1単語として認識されるため、ストップワードにすることで除外する
			summary = summarizer(document=parser.document, sentences_count=sentences_count)

			#print('  SUMMARY : {0}'.format(summary))

			# 元の文を表示
			for sentence in summary:
				print('{0}'.format(sentences[corpus.index(sentence.__str__())]))

		fp.close()

if __name__ == '__main__' :
	main()
