all : init

init :
	python3 add_file_to_knowledge.py -n example files/*.md

clean :
	python3 delete_files.py
	python3 delete_knowledges.py

normalize:
	find ./files -type f -name "*.md" -print -exec python3 zen2han.py -o {} {} \;

async:
	./chat_completions_async.py template.shrc 2>debug.log

