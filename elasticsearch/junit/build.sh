#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd ${top_dir}
    
es_host="192.168.0.98:9200"
kbn_host="192.168.0.98:5601"

index="junit_report-0001"
pretty="?pretty"

data_view="junit_report"

workdir="work"
src_dir="${workdir}/source"
build_root="${workdir}/build"

vers="2.17 2.18 2.19 2.20 2.21 2.22 2.23 2.24 2.26 2.27 2.50 2.51 2.52"
vers="$vers 2.53 2.55 2.57 2.58 2.59"
#vers="$vers 2.92 2.93 2.94 2.96"
#vers="$vers 4.00 4.01 4.02 4.03 4.04 4.05 4.06 4.07 4.08 4.09 4.10"

#urls="$urls https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/JSON-4.10.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/JSON-2.91_01.tar.gz"

usage()
{
    cat - << EOS
usage : $0 [options] target1 target2 ...

  target
    json
    merge

    index
    delete_index
    create_view
    delete_view

    summary, json, upload
EOS
}

help()
{
    usage
}

all()
{
    :
}

fetch()
{
  mkdir -p ${src_dir}

  for ver in ${vers}; do
    #url="https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI"
    #url="$url/JSON-${ver}.tar.gz"
    url="https://github.com/makamaka/JSON/archive/refs/tags/${ver}.tar.gz"

    filename="JSON-${ver}.tar.gz"

    if [ -e "${src_dir}/${filename}" ]; then
      echo "skip ${filename}"
      continue
    fi
    cmd="curl -L -o ${src_dir}/${filename} ${url}"
    echo $cmd
    $cmd
  done
}

extract()
{
  mkdir -p ${build_root}

  for ver in ${vers}; do
    filepath="$(realpath ${src_dir}/JSON-${ver}.tar.gz)"

    if [ ! -d "${build_root}/JSON-${ver}" ]; then
      cmd="tar -C ${build_root} -xf ${filepath}"
      echo $cmd
      $cmd
    else
      echo "skip extracting ${filepath}"
    fi
  done
}

get_dirname()
{
    url=$1
    shift
    
    #echo "DEBUG : ${url}"

    filename=$(basename ${url})
    dirname=""

    case ${filename} in
        *.tar.gz )
            dirname=$(basename ${filename} .tar.gz)
            ;;
        * )
            echo "unknown extension, ${filename}"
            exit 1
            ;;
    esac

    echo "$dirname"
}

build()
{
  for ver in ${vers}; do
    build_dir="${build_root}/JSON-${ver}"
    if [ ! -d "${build_dir}" ]; then
      echo "ERROR: no such directory, ${build_dir}"
      continue
    fi

    cd ${build_dir}
    perl Makefile.PL
    make
    cd ${top_dir}
  done
}

check()
{
  for ver in ${vers}; do
    build_dir="${build_root}/JSON-${ver}"
    if [ ! -d "${build_dir}" ]; then
      echo "ERROR: no such directory, ${build_dir}"
      continue
    fi

    cd ${build_dir}
    echo "run prove in ${build_dir}"
    prove --timer -I blib/lib -I blib/arch \
      --formatter TAP::Formatter::JUnit > junit_report.xml 2>&1
    cd ${top_dir}
  done
}

json()
{
  xmlfiles=$(find ./work -name "junit_report.xml" | sort)

  for xmlfile in $xmlfiles; do
    jsonfile=$(echo $xmlfile | sed -e 's|.xml$|.jsonl|')
    module=$(dirname $xmlfile | sed 's|.*/||')

    cmd="python3 junit2jsonl.py -o $jsonfile -m $module $xmlfile"
    echo $cmd
    $cmd
  done
}

db()
{
  xmlfiles=$(find ./work -name "junit_report.xml" | sort)

  for xmlfile in $xmlfiles; do
    database=$(echo $xmlfile | sed -e 's|.xml$|.db|')
    cmd="python3 junit2db.py -o $database $xmlfile"
    echo $cmd
    $cmd
  done
}


merge()
{
  jsonfiles=$(find ./work -name "junit_report.jsonl" | sort)

  merged="junit_report.jsonl"
  rm -f $merged
  for jsonfile in $jsonfiles; do
    cat $jsonfile >> $merged
  done
}

delete_view()
{
  curl -n \
    --silent \
    -o views.json \
    -H 'Content-Type: application/json' \
    -XGET "https://${kbn_host}/kibana/api/data_views"

  #cat views.json | python3 -m json.tool

  #cat views.json | jq -r '.data_view[] | .id + "," + .name'

  # get id of data view 'junit_report'
  id=`cat views.json | jq -r '[.data_view[]]' | \
    jq "map(select( .name == \"JUnit Report\"))" | jq -r ' .[].id'`
  echo id of data view $data_view is $id
  
  curl -n \
    -H "kbn-xsrf: reporting" \
    -XDELETE "https://${kbn_host}/kibana/api/data_views/data_view/${id}"
}

view()
{
  curl -n \
    --silent \
    -H 'Content-Type: application/json' \
    -H "kbn-xsrf: reporting" \
    -o data_view.log \
    -XPOST "https://${kbn_host}/kibana/api/data_views/data_view?pretty" \
    --data-binary @- << EOS
{
  "data_view" : {
    "title" : "junit_report-*",
    "name"  : "JUnit Report",
    "version" : "0.0.1"
  }
}
EOS
  
  cat data_view.log
}

delete_view()
{
  curl -n \
    -H "kbn-xsrf: reporting" \
    -XDELETE "https://${kbn_host}/kibana/api/data_views/data_view/${data_view}"
}

destroy()
{
  delete
  delete_data_view
}


mapping()
{
   curl -n \
     -H 'Content-Type: application/json' \
     -XPUT "https://${es_host}/${index}" \
     --data @- << EOS
{
  "mappings" : {
    "properties" : {
      "testsuite.@name" : { "type": "text" },
      "testsuite.error.@message" : { "type": "text" },
      "testsuite.module" : { "type": "keyword", "index" : true },
      "testsuite.system-err" : { "type": "text" },
      "testsuite.system-out" : { "type": "text" },
      "testsuite.@tests" : { "type": "integer" },
      "testsuite.@errors" : { "type": "integer" },
      "testsuite.@failures" : { "type": "integer" }
    }
  }
}
EOS

}


index()
{
  pretty=""
  curl -n --silent -H 'Content-Type: application/json' \
    -XPOST "https://${es_host}/${index}/_bulk${pretty}" \
    --data-binary "@junit_report.jsonl" \
    -o junit_report.log
}

delete_index()
{
  curl -n \
    -XDELETE "https://${es_host}/${index}?pretty"
}



old_check()
{
    for url in ${urls}; do
        filename=$(basename ${url})
        
        dirname=`get_dirname ${url}`

        cd ${build_dir}/${dirname}
        if [ -e "Build.PL" ]; then
            build_type="Module::Build"
        elif [ -e "Makefile.PL" ]; then
            build_type="ExtUtils::MakeMaker"
        else
            echo "can not determine build tool in ${dirname}"
            exit 1
        fi

        if [ "$build_type" = "Module::Build" ]; then
            #./Build test
            if [ $force_check -ne 0 -o ! -e "junit_report.xml" ]; then
              echo "run prove in ${dirname}"
              prove --timer -I blib/lib -I blib/arch \
                --formatter TAP::Formatter::JUnit t/* > junit_report.xml \
                2>/dev/null
            else
              echo "skip prove in ${dirname}"
            fi
        elif [ "$build_type" = "ExtUtils::MakeMaker" ]; then
            if [ $force_check -ne 0 -o ! -e "junit_report.xml" ]; then
              echo "run prove in ${dirname}"
              prove --timer -I blib/lib -I blib/arch \
                --formatter TAP::Formatter::JUnit t/* > junit_report.xml \
                2>&1
            else
              echo "skip prove in ${dirname}"
            fi
        else
            echo "can not determine build tool in ${dirname}"
            exit 1
        fi

        cd ${top_dir}
    done
}

pipeline()
{
   curl -n \
     -H 'Content-Type: application/json' \
     -XPUT "https://${es_host}/_ingest/pipeline/ingest_timestamp" \
     --data @- << EOS
{
  "processors" : [
    {
      "set": {
        "field": "@timestamp",
        "value": "{{_ingest.timestamp}}"
      }
    }
  ]
}
EOS

}

show_pipeline()
{
   curl -n \
     -XGET "https://${es_host}/_ingest/pipeline?pretty"
     #-XGET "https://${es_host}/_ingest/pipeline/ingest_timestamp"
}

delete_pipeline()
{
   curl -n \
     -H 'Content-Type: application/json' \
     -XDELETE "https://${es_host}/_ingest/pipeline/ingest_timestamp"
}

summarize()
{
    rm -f junit_report.xml
    xsdfile="mod-junit-10.xsd"
    #xsdfile="jenkins-junit.xsd"

    cmd="junitcat -d -x ${xsdfile} -o junit_report.xml work/"
    echo $cmd
    $cmd
}

summary()
{
    summarize
}

debug()
{
    #xmlfile="work/build/YAML-1.30/junit_report.xml"
    #xmlfile="work/build/V-0.16/junit_report.xml"
    #xmlfile="work/build/DateTime-1.59/junit_report.xml"
    xmlfile="work/build/Data-Dumper-2.183/junit_report.xml"

    #xsdfile="/usr/share/xunit-plugin/resources/types/model/xsd/junit-10.xsd"
    #xsdfile="./mod-junit-10.xsd"
    xsdfile="jenkins-junit.xsd"

    xmllint --noout --schema $xsdfile $xmlfile
}

old_json()
{

    cmd="python3 junit2jsonl.py"
    cmd="$cmd -o junit_report.jsonl junit_report.xml"
    echo $cmd
    $cmd
}

delete()
{
    pretty=""
    curl -n -H 'Content-Type: application/json' \
        -XDELETE "https://${es_host}/${index}"
}


if [ "$#" = "0" ]; then
  usage
  exit 1
fi

args=""

force_check=0

while [ "$#" -ne 0 ]; do
  case "$1" in
    h)
      usage
	  ;;
    v)
      verbose=1
	  ;;
    -f | --force-check )
      force_check=1
      ;;
    *)
	  args="$args $1"
	  ;;
  esac

  shift

done

for target in $args ; do
  LANG=C type $target | grep function > /dev/null 2>&1
  if [ "$?" = "0" ]; then
    $target
  else
    echo "$target is not a shell function"
  fi
done

