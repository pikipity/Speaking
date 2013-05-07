; 脚本由 Inno Setup 脚本向导 生成！
; 有关创建 Inno Setup 脚本文件的详细资料请查阅帮助文档！

#define MyAppName "Happy Birthday"
#define MyAppVersion "1.0"
#define MyAppPublisher "pikipity"
#define MyAppURL "pikipity.github.io"

[Setup]
; 注: AppId的值为单独标识该应用程序。
; 不要为其他安装程序使用相同的AppId值。
; (生成新的GUID，点击 工具|在IDE中生成GUID。)
AppId={{4D250656-D490-46F6-B66A-CC7ED17D7E39}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
InfoBeforeFile=C:\Documents and Settings\Administrator\My Documents\GitHub\Speaking\happy birthday
InfoAfterFile=C:\Documents and Settings\Administrator\My Documents\GitHub\Speaking\Readme.markdown
OutputDir=C:\Documents and Settings\Administrator\My Documents\GitHub\Speaking\pack
OutputBaseFilename=Happy Birthday
SetupIconFile=C:\Documents and Settings\Administrator\My Documents\GitHub\Speaking\icon\cake.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "C:\Documents and Settings\Administrator\My Documents\GitHub\Speaking\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 注意: 不要在任何共享系统文件上使用“Flags: ignoreversion”

[Icons]
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

