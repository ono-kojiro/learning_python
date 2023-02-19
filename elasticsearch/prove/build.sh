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
build_dir="${workdir}/build"

urls=""
urls="$urls https://cpan.metacpan.org/authors/id/A/AB/ABELTJE/V-0.16.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/XML-LibXML-2.0208.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/DBD-SQLite-1.72.tar.gz"
#urls="$urls https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/JSON-4.10.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/JSON-2.91_01.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/T/TI/TINITA/YAML-1.30.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/K/KA/KARUPA/TOML-0.97.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/K/KA/KARUPA/TOML-Parser-0.91.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/Types-Serialiser-1.01.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/common-sense-3.75.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/G/GA/GAAS/Unicode-Map8-0.13.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/Text-CSV-2.02.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/Time-HiRes-1.9764.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/DateTime-1.59.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/E/EX/EXODIST/Test-Simple-1.302191.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/N/NW/NWCLARK/Data-Dumper-2.183.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Path-Tiny-0.144.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/R/RM/RMBARKER/File-Rename-2.00_3.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/J/JO/JONASS/App-Licensecheck-v3.3.4.tar.gz"
urls="$urls https://cpan.metacpan.org/authors/id/N/NW/NWCLARK/Data-Dumper-2.183.tar.gz"

usage()
{
    cat - << EOS
usage : $0 [options] target1 target2 ...

  target
    fetch, extract, build, check

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

    for url in ${urls}; do
        filename=$(basename ${url})
        if [ -e "${src_dir}/${filename}" ]; then
            echo "skip ${filename}"
            continue
        fi
        cmd="curl -o ${src_dir}/${filename} ${url}"
        echo $cmd
        $cmd
    done
}

extract()
{
    mkdir -p ${build_dir}

    for url in ${urls}; do
        filename=$(basename ${url})
        filepath=$(realpath ${src_dir}/${filename})

        case ${filename} in
            *.tar.gz )
                dirname=$(basename ${filename} .tar.gz)
                ;;
            * )
                echo "unknown extension, ${filename}"
                exit 1
                ;;
        esac
        
        if [ ! -e "${build_dir}/${dirname}" ]; then
            cmd="tar -C ${build_dir} -xf ${filepath}"
            echo $cmd
            $cmd
        else
            echo "skip extract ${dirname}"
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
    for url in ${urls}; do
        filename=$(basename ${url})
        echo "url is ${url}"
        dirname=`get_dirname ${url}`

        build_type="unknown"

        cd ${build_dir}/${dirname}
        if [ -e "Build.PL" ]; then
            build_type="Module::Build"
        elif [ -e "Makefile.PL" ]; then
            build_type="ExtUtils::MakeMaker"
        else
            pwd
            echo "can not determine build tool in ${dirname}"
            exit 1
        fi

        if [ "$build_type" = "Module::Build" ]; then
            cmd="perl Build.PL"
            if [ ! -e "Build" ]; then
                echo "run '$cmd'"
                $cmd
            else
                echo "skip '$cmd'"
            fi

            ./Build
        elif [ "$build_type" = "ExtUtils::MakeMaker" ]; then
            cmd="perl Makefile.PL"
            if [ ! -e "Makefile" ]; then
                echo "run '$cmd'"
                $cmd
            else
                echo "skip '$cmd'"
            fi
            make
        else
            pwd
            echo "can not determine build tool in ${dirname}"
            exit 1
        fi

        cd ${top_dir}
    done
}

check()
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

json()
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


upload()
{
    pretty=""
    curl -n -H 'Content-Type: application/json' \
        -XPOST "https://${es_host}/${index}/_bulk${pretty}" \
        --data-binary "@junit_report.jsonl"
}

data_view()
{
  curl -n \
    -H 'Content-Type: application/json' \
    -H "kbn-xsrf: reporting" \
    -XPOST "https://${kbn_host}/kibana/api/data_views/data_view?pretty" \
    --data-binary @- << EOS
{
  "data_view" : {
    "id"    : "${data_view}",
    "version" : "0.0.1",
    "title" : "junit_report-*",
    "name"  : "JUnit Report"
  }
}
EOS

}

delete_data_view()
{
  curl -n \
    -H "kbn-xsrf: reporting" \
    -XDELETE "https://${kbn_host}/kibana/api/data_views/data_view/${data_view}"
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

