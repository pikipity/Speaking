; �ű��� Inno Setup �ű��� ���ɣ�
; �йش��� Inno Setup �ű��ļ�����ϸ��������İ����ĵ���

#define MyAppName "Happy Birthday"
#define MyAppVersion "1.0"
#define MyAppPublisher "pikipity"
#define MyAppURL "pikipity.github.io"

[Setup]
; ע: AppId��ֵΪ������ʶ��Ӧ�ó���
; ��ҪΪ������װ����ʹ����ͬ��AppIdֵ��
; (�����µ�GUID����� ����|��IDE������GUID��)
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
; ע��: ��Ҫ���κι���ϵͳ�ļ���ʹ�á�Flags: ignoreversion��

[Icons]
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

