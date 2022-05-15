<!-- : Begin batch script
@ECHO OFF
@SETLOCAL ENABLEDELAYEDEXPANSION

SET PATH=%SYSTEMROOT%\System32
CALL C:\opt\PortableGit-2.36.1-64-bit.bat
CALL C:\opt\python-3.10.4-embed-amd64.bat

REM SET TITLE=bocchan
REM SET TITLE=hashire_merosu
REM SET TITLE=chumonno_oi_ryoriten
REM SET TITLE=karamazofuno_kyodai_01
SET TITLE=gingatetsudono_yoru

IF "!TITLE!" == "bocchan" (
  SET URL=https://www.aozora.gr.jp/cards/000148/files/752_ruby_2438.zip
) ELSE IF "!TITLE!" == "hashire_merosu" (
  SET URL=https://www.aozora.gr.jp/cards/000035/files/1567_ruby_4948.zip
) ELSE IF "!TITLE!" == "chumonno_oi_ryoriten" (
  SET URL=https://www.aozora.gr.jp/cards/000081/files/43754_ruby_17594.zip
) ELSE IF "!TITLE!" == "karamazofuno_kyodai_01" (
  SET URL=https://www.aozora.gr.jp/cards/000363/files/42286_ruby_36920.zip
) ELSE IF "!TITLE!" == "gingatetsudono_yoru" (
SET URL=https://www.aozora.gr.jp/cards/000081/files/456_ruby_145.zip
) ELSE (
  ECHO ERROR : invalid title, !TITLE!
  EXIT /B 1
)


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

ENDLOCAL & SET ERRORLEVEL=%ERRORLEVEL%
@ECHO ON
@EXIT /B !ERRORLEVEL!

REM ===============================
REM === All
REM ===============================
:ALL
CALL :FETCH
CALL :PREPARE
CALL :TEST
GOTO :EOF

REM ===============================
REM === Help
REM ===============================
:HELP
ECHO "Usage : build.bat command [command...]"
GOTO :EOF

REM ===============================
REM === Version
REM ===============================
:VERSION
git --version
python --version
GOTO :EOF

REM ===============================
REM === Setup
REM ===============================
:SETUP
python -m pip install janome
python -m pip install tinysegmenter
python -m pip install sumy
python -m pip install jaconv

GOTO :EOF

REM ===============================
REM === Fetch
REM ===============================
:FETCH
python fetch.py !URL!
GOTO :EOF


REM ===============================
REM === Prepare
REM ===============================
:PREPARE
python remove_ruby.py -e cp932 -o out/!TITLE!_mod.txt out/!TITLE!.txt
GOTO :EOF

REM ===============================
REM === Test
REM ===============================
:TEST
python summarize.py out/!TITLE!_mod.txt
GOTO :EOF

REM ===============================
REM === Clean
REM ===============================
:CLEAN
ECHO This is clean.
CSCRIPT //NOLOGO "%~f0?.wsf" //job:Clean
@GOTO :EOF

REM ===============================
REM === _CHECK_LABEL
REM ===============================
:_CHECK_LABEL
FINDSTR /I /R /C:"^[ ]*:%1\>" "%~f0" >NUL 2>NUL
@GOTO :EOF

----- Begin wsf script --->
<package>
	<job id="Main">
		<?job debug="true"?>
		<script language="JavaScript">
			WScript.Echo("Hello JavaScript World");
			WScript.Quit(0);
		</script>
	</job>

	<job id="Clean">
		<?job debug="true"?>
		<script language="JavaScript">
			WScript.Echo("This is clean job");
			WScript.Quit(0);
		</script>
	</job>
</package>
