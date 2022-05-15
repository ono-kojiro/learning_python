<!-- : Begin batch script
@ECHO OFF
@SETLOCAL ENABLEDELAYEDEXPANSION

SET PATH=%SYSTEMROOT%\System32
CALL PortableGit-2.36.1-64-bit.bat
CALL python-3.10.4-embed-amd64.bat

CALL C:\opt\cuda-v11.7.bat
CALL C:\opt\cudnn-windows-x86_64-8.4.0.27_cuda11.6.bat

echo INFO : first ERRORLEVEL is !ERRORLEVEL!

IF "x%1" == "x" (
	CALL :ALL
	REM disable echo because subroutine might enable echo
	@ECHO OFF
	IF !ERRORLEVEL! NEQ 0 (
		ECHO ERROR : ALL returned !ERRORLEVEL!
		EXIT /B !ERRORLEVEL!
	)
) ELSE (
	FOR %%i IN (%*) DO (
		ECHO check %%i ...
		
		CALL :_CHECK_LABEL %%i
		ECHO CALL :_CHECK_LABEL returned !ERRORLEVEL!
		IF !ERRORLEVEL! == 0 (
			ECHO call :%%i ...
			CALL :%%i
			REM disable echo because subroutine might enable echo
			@ECHO OFF

			IF !ERRORLEVEL! NEQ 0 (
				ECHO ERROR : %%i returned !ERRORLEVEL!
				EXIT /B !ERRORLEVEL!
			)
		) ELSE (
			CALL :_DEFAULT "%%1"
			IF !ERRORLEVEL! NEQ 0 (
				ECHO ERROR : _DEFAULT %%i returned !ERRORLEVEL!
				EXIT /B !ERRORLEVEL!
			)
		)
		
		ECHO current errorlevel is !ERRORLEVEL!
		ECHO check finished
		
	)
)

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
  -o test_image10.png ^
  -n 10 ^
  fashion-mnist/data/fashion/t10k-images-idx3-ubyte.gz

GOTO :EOF

REM ===============================
REM === Predict
REM ===============================
:PREDICT
SET TF_CPP_MIN_LOG_LEVEL=2
python predict.py test_image10.png
GOTO :EOF

REM ===============================
REM === Clean
REM ===============================
:CLEAN
ECHO This is clean.
CSCRIPT //NOLOGO "%~f0?.wsf" //job:Clean
@GOTO :EOF

REM ===============================
REM === _DEFAULT
REM ===============================
:_DEFAULT
python predict.py %1
EXIT /B !ERRORLEVEL!

REM ===============================
REM === _CHECK_LABEL
REM ===============================
:_CHECK_LABEL
ECHO check label "%1" in %~f0 ...
FINDSTR /I /R /C:"^[ ]*:%1\>" "%~f0"
ECHO findstr returned !ERRORLEVEL!
EXIT /B !ERRORLEVEL!

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
