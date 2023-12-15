;!define version "1.0.1" use /D if possible to pass in version info.
;!define ui_name "Cochleogram"
;!define package "cochleogram"
;!define script "cochleogram.exe"
!include nsDialogs.nsh
!include MUI2.nsh


Name "${ui_name}"
OutFile "dist/${package}-${version}.exe"
InstallDir "$LocalAppData\${package}-${version}"

RequestExecutionLevel user
ShowInstDetails show

Var /global key

!define MUI_FINISHPAGE_NOAUTOCLOSE true
!define MUI_ICON '${install_icon_path}'
!define MUI_UNICON '${install_icon_path}'


!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"


Section ""
	SetOutPath $INSTDIR
	File /r "build\pyinstaller\${package}"

    WriteUninstaller "$INSTDIR\uninstall.exe"
    ; First, create key in registry that will show up in Add/Remove programs
    StrCpy $key "Software\Microsoft\Windows\CurrentVersion\Uninstall\${package}-${version}"
    WriteRegStr SHCTX $key "DisplayName" "${ui_name} ${version}"
    WriteRegStr SHCTX $key "DisplayIcon" "$INSTDIR\${package}\${icon_path}"
    WriteRegStr SHCTX $key "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr SHCTX $key "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"

	createShortCut "$SMPROGRAMS\${ui_name} ${version}.lnk" "$INSTDIR\${package}\${script}" "" "$INSTDIR\${package}\_internal\${icon_path}"
SectionEnd

Section "uninstall"
    StrCpy $key "Software\Microsoft\Windows\CurrentVersion\Uninstall\${package}-${version}"

    ; Remove uninstaller from registry so it doesn't show up under Add/Remove programs
  	DeleteRegKey SHCTX $key
	Delete "$SMPROGRAMS\${ui_name} ${version}.lnk"
	rmdir /r $INSTDIR
SectionEnd
