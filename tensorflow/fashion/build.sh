#!/usr/bin/env sh

. ./pyenv.bashrc

set -e
top_dir="$(cd "$(dirname "$0")" > /dev/null 2>&1 && pwd)"
cd $top_dir

script=$(basename "$0")

do_usage()
{
  cat - << EOS
usage : $script [options] command [args]

  options
    -h, --help     show this message
    -v, --verbose  verbose mode

  command
    prepare     innstall tensorflow module
    train       train model
    evaluate    evaluate model
    extract     extract test image No.9
    predict     read test_image9.png and predict
    mclean      remove models, checkpoints

EOS

}

do_help()
{
  do_usage
}

do_prepare()
{
  python3 -m pip install tensorflow
  python3 -m pip install pillow

  if [ ! -e "fashion-mnist" ]; then
    git clone https://github.com/zalandoresearch/fashion-mnist.git
  fi
}

do_train()
{
  TF_CPP_MIN_LOG_LEVEL=2 ./train.py
}

do_evaluate()
{
  TF_CPP_MIN_LOG_LEVEL=2 ./evaluate.py
}

do_extract()
{
  ./extract_image.py \
    -o test_image9.png \
    -n 9 \
    fashion-mnist/data/fashion/t10k-images-idx3-ubyte.gz
}

do_predict()
{
  TF_CPP_MIN_LOG_LEVEL=2 ./predict.py test_image9.png
}

do_mclean()
{
  rm -rf models
  rm -rf checkpoints
  rm -rf fashion-mnist
  rm -f  test_image9.png
}

all()
{
  :
}

cmd=""
verbose=""

# parse global options
while [ "$#" -ne 0 ]; do
  case $1 in
    -h )
	  do_usage
      exit 1
      ;;
    -v )
      verbose=1
      ;;
    -* )
	  echo "ERROR : unknown option, $1"
	  exit 1
      ;;
    * )
	  cmd=$1
	  shift
	  break
      ;;
  esac
  
  shift
done

if [ -z "$cmd" ]; then
  do_usage
  exit 1
fi

func_name="do_${cmd}"

num=`LANG=C type "do_${cmd}" | grep 'function' | wc -l`

if [ "$num" -ne 0 ]; then
  do_${cmd} "$@"
else
  echo "ERROR : no such command, $cmd"
  exit 1
fi

