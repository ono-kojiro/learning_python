<!-- : Begin batch script
@ECHO OFF
@SETLOCAL ENABLEDELAYEDEXPANSION

SET PATH=%SYSTEMROOT%\System32
CALL C:\opt\python-3.13.2-embed-amd64.bat

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
	)
)

@ECHO ON
@EXIT /B !ERRORLEVEL!

REM ===============================
REM === All
REM ===============================
:ALL
CALL :BUILD
CALL :WAV
GOTO :EOF

REM ===============================
REM === Help
REM ===============================
:HELP
ECHO "Usage : build.bat command [command...]"
GOTO :EOF

REM ===============================
REM === Build
REM ===============================
:BUILD
python show_voices.py
GOTO :EOF

REM ===============================
REM === Wav
REM ===============================
:WAV
python generate.py -o sayaka.wav input.txt
GOTO :EOF

REM ===============================
REM === _DEFAULT
REM ===============================
:_DEFAULT
CALL :ALL
EXIT /B !ERRORLEVEL!

REM ===============================
REM === _CHECK_LABEL
REM ===============================
:_CHECK_LABEL
ECHO check label "%1" in %~f0 ...
FINDSTR /I /R /C:"^[ ]*:%1\>" "%~f0"
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
