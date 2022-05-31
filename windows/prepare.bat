@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

ECHO cwd is %~dp0

CALL python-3.10.4-embed-amd64.bat
CALL strawberry-perl-5.32.1.1-64bit-portable.bat

IF "x%1" == "x" (
	CALL :ALL
	REM disable echo because subroutine might enable echo
	@ECHO OFF
	IF NOT !ERRORLEVEL! == 0 (
		ECHO ERROR : ALL returned !ERRORLEVEL!
		EXIT /B !ERRORLEVEL!
	)
) else (
	FOR %%i IN (%*) DO (
		ECHO check label %%i
		CALL :_CHECK_LABEL %%i
		IF !ERRORLEVEL! == 0 (
			CALL :%%i
			REM disable echo because subroutine might enable echo
			@ECHO OFF

			IF NOT !ERRORLEVEL! == 0 (
				ECHO ERROR : %%i returned !ERRORLEVEL!
				EXIT /B !ERRORLEVEL!
			)
		) ELSE (
			ECHO ERROR : no such label, "%%i"
			EXIT /B 1
		)
		
	)
)

@ECHO ON
@ECHO final errorlevel is %ERRORLEVEL%
@EXIT /B %ERRORLEVEL%

REM ===============================
REM === All
REM ===============================
:ALL
ECHO This is all.
CALL :BUILD
GOTO :EOF

REM ===============================
REM === Fetch
REM ===============================
:FETCH

IF NOT EXIST download ( MD download )
CD download

IF NOT EXIST python-3.10.4-embed-amd64.zip (
  curl -L -O ^
    https://www.python.org/ftp/python/3.10.4/python-3.10.4-embed-amd64.zip
) ELSE (
  ECHO skip python-3.10.4-embed-amd64.zip
)

curl -L -O https://bootstrap.pypa.io/get-pip.py


IF NOT EXIST strawberry-perl-5.32.1.1-64bit-portable.zip (
  curl -L -O ^
    https://strawberryperl.com/download/5.32.1.1/strawberry-perl-5.32.1.1-64bit-portable.zip
) ELSE (
  ECHO skip strawberry-perl-5.32.1.1-64bit-portable.zip
)

IF NOT EXIST PortableGit-2.36.1-64-bit.7z.exe (
  curl -L -O ^
    https://github.com/git-for-windows/git/releases/download/v2.36.1.windows.1/PortableGit-2.36.1-64-bit.7z.exe
) ELSE (
  ECHO skip PortableGit-2.36.1-64-bit.7z.exe
)



IF NOT EXIST win-svn-1.14.2.tar.gz (
  curl -L -o win-svn-1.14.2.tar.gz https://github.com/nono303/win-svn/archive/refs/tags/1.14.2.tar.gz
) ELSE (
  ECHO skip win-svn-1.14.2.tar.gz
)

CD ..

GOTO :EOF

REM ===============================
REM === Extract
REM ===============================
:EXTRACT
IF NOT EXIST tools ( MD tools )

IF NOT EXIST tools\python-3.10.4-embed-amd64 (
  unzip -d tools\python-3.10.4-embed-amd64 ^
           download\python-3.10.4-embed-amd64.zip
) ELSE (
  ECHO skip python
)

IF NOT EXIST tools\strawberry-perl-5.32.1.1-64bit-portable (
  unzip -d tools\strawberry-perl-5.32.1.1-64bit-portable ^
           download\strawberry-perl-5.32.1.1-64bit-portable.zip
) ELSE (
  ECHO skip perl
)

CD ..

GOTO :EOF


REM ===============================
REM === Build
REM ===============================
:BUILD
ECHO This is build.
GOTO :EOF

REM ===============================
REM === Test
REM ===============================
:TEST
ECHO test
perl -p -i -e "s/#import site/import site/" tools/python-3.10.4-embed-amd64/python310._pth

python download/get-pip.py

GOTO :EOF


REM ===============================
REM === Update
REM ===============================
:UPDATE
python -m pip install openpyxl
python -m pip install numpy

GOTO :EOF

REM ===============================
REM === HOGE
REM ===============================
:HOGE
perl --version
ECHO after perl
CALL cpanm.bat -v --notest OLE::Storage_Lite
CALL cpanm.bat -v --notest Spreadsheet::ParseExcel
CALL cpanm.bat -v --notest Spreadsheet::XLSX
CALL cpanm.bat -v --notest Excel::Writer::XLSX
CALL cpanm.bat -v --notest Crypt::RC4
CALL cpanm.bat -v --notest Digest::Perl::MD5
CALL cpanm.bat -v --notest Unicode::Map
CALL cpanm.bat -v --notest Unicode::Japanese
GOTO :EOF

REM ===============================
REM === _CHECK_LABEL
REM ===============================
:_CHECK_LABEL
ECHO DEBUG file is %~f0
FINDSTR /I /R /C:"^[ ]*:%1\>" "%~f0"
ECHO ERRORLEVEL is %ERRORLEVEL%
GOTO :EOF

