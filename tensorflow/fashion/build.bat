<!-- : Begin batch script
@ECHO OFF
@SETLOCAL ENABLEDELAYEDEXPANSION

SET PATH=%SYSTEMROOT%\System32
CALL PortableGit-2.36.1-64-bit.bat
CALL python-3.10.4-embed-amd64.bat

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
CALL :PREPARE
CALL :TRAIN
CALL :EVALUATE
CALL :EXTRACT
CALL :PREDICT
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
ECHO %PATH%
git --version
python --version
GOTO :EOF

REM ===============================
REM === Prepare
REM ===============================
:PREPARE
IF NOT EXIST fassion-mnist (
  git clone https://github.com/zalandoresearch/fashion-mnist.git
)
GOTO :EOF

REM ===============================
REM === Train
REM ===============================
:TRAIN
SET TF_CPP_MIN_LOG_LEVEL=2
python train.py
GOTO :EOF

REM ===============================
REM === Evaluate
REM ===============================
:EVALUATE
SET TF_CPP_MIN_LOG_LEVEL=2
python evaluate.py
GOTO :EOF

REM ===============================
REM === Extract
REM ===============================
:EXTRACT
python extract_image.py ^
  -o test_image9.png ^
  -n 9 ^
  fashion-mnist/data/fashion/t10k-images-idx3-ubyte.gz

GOTO :EOF

REM ===============================
REM === Predict
REM ===============================
:PREDICT
SET TF_CPP_MIN_LOG_LEVEL=2
python predict.py test_image9.png
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
