@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

SET PATH=%SYSTEMROOT%\System32

CALL C:\opt\PortableGit-2.36.1-64-bit.bat
CALL C:\opt\python-3.10.4-embed-amd64.bat
CALL C:\opt\strawberry-perl-5.32.1.1-64bit-portable.bat

IF "x%1" == "x" (
	CALL :ALL
	IF !ERRORLEVEL! NEQ 0 (
		ECHO ERROR : ALL returned !ERRORLEVEL!
	) ELSE (
		ECHO INFO  : ALL returned !ERRORLEVEL!
	)
) ELSE (
	FOR %%i IN (%*) DO (
		CALL :_CHECK_LABEL %%i
		IF !ERRORLEVEL! == 0 (
			CALL :%%i
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

SET RETVAL=!ERRORLEVEL!
ENDLOCAL && SET RETVAL=%ERRORLEVEL%

EXIT /B %RETVAL%

REM ===============================
REM === All
REM ===============================
:ALL
CALL :BUILD
EXIT /B !ERRORLEVEL!

REM ===============================
REM === Help
REM ===============================
:HELP
perl --version
git --version
python --version
GOTO :EOF

REM ===============================
REM === Build
REM ===============================
:BUILD
GOTO :EOF

REM ===============================
REM === OK
REM ===============================
:OK
EXIT /B 0
GOTO :EOF

REM ===============================
REM === NG
REM ===============================
:NG
EXIT /B 1
GOTO :EOF

REM ===============================
REM === _DEFAULT
REM ===============================
:_DEFAULT
EXIT /B !ERRORLEVEL!

REM ===============================
REM === _CHECK_LABEL
REM ===============================
:_CHECK_LABEL
FINDSTR /I /R /C:"^[ ]*:%1\>" "%~f0" >NUL 2>NUL
EXIT /B !ERRORLEVEL!
