#!/bin/sh

package=""
version=""
indir=""
outdir=""

make_package()
{
  ret=0

  package="$1"
  version="$2"
  indir="$3"
  outdir="$4"

  if [ -z "$package" ]; then
    echo "ERROR: no package option" 1>&2
    ret=`expr $ret + 1`
  fi

  if [ -z "$version" ]; then
    echo "ERROR: no version option" 1>&2
    ret=`expr $ret + 1`
  fi
  
  if [ -z "$indir" ]; then
    echo "ERROR: no indir option" 1>&2
    ret=`expr $ret + 1`
  fi
  
  if [ -z "$outdir" ]; then
    echo "ERROR: no outdir option" 1>&2
    ret=`expr $ret + 1`
  fi

  if [ "$ret" -ne 0 ]; then
    exit $ret
  fi

  maintainer=`git config --get user.name`
  email=`git config --get user.email`

  mkdir -p $indir/DEBIAN
  cat << EOS > $indir/DEBIAN/control
Package: $package
Maintainer: $maintainer <$email>
Architecture: all
Version: $version
Depends: python3-pip
Description: $package
EOS

  #cp -f postinst $destdir/DEBIAN/
  #cp -f postrm   $destdir/DEBIAN/
  #cp -f prerm    $destdir/DEBIAN/
  fakeroot dpkg-deb --build -Z gzip $indir $outdir
}

args=""

while [ "$#" -ne 0 ]; do
  case $1 in
    -h )
      ;;
    -p | --package )
      shift
      package="$1"
      ;;
    -v | --version )
      shift
      version="$1"
      ;;
    -i | --indir )
      shift
      indir="$1"
      ;;
    -o | --outdir )
      shift
      outdir="$1"
      ;;
    * )
      echo "ERROR: invalid argument, $1"
      ;;
  esac
  shift
done

#if [ "$#" -eq 0 ]; then
#  all
#fi

#for target in "$@"; do
#    LANG=C type $target | grep 'function' > /dev/null 2>&1
#    if [ $? -eq 0 ]; then
#        $target
#    else
#        echo invalid target, "$target"
#    fi
#done

make_package \
  "${package}" \
  "${version}" \
  "${indir}" \
  "${outdir}"



