@echo off
:: Check if the script is running as administrator
:: If not, prompt the user to run it as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrative privileges.
    echo Please run this script as an administrator.
    pause
    exit /b
)

:: Prompt for the username
set /p username="Enter the username for which you want to change the password: "

:: Check if the user exists
net user %username% >nul 2>&1
if %errorLevel% neq 0 (
    echo User "%username%" does not exist.
    pause
    exit /b
)

:: Prompt for the new password
set /p password="Enter the new password for user %username%: "

:: Change the user's password
net user %username% %password%
if %errorLevel% equ 0 (
    echo Password for user "%username%" has been changed successfully.
) else (
    echo Failed to change the password. Please check your input and try again.
)

pause
exit /b
