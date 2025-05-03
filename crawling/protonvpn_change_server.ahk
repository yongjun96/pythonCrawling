#Requires AutoHotkey v2.0

SetTitleMatchMode(2)  ; 부분 일치 허용

if WinExist("Proton VPN")
{
    WinActivate("Proton VPN")
    Sleep(1000)

    ; 예: Change Server 버튼 위치 클릭
    Click(691, 147)

        Sleep(3000)

    Click(621, 159)
}
else
{
    MsgBox("ProtonVPN 창을 찾을 수 없습니다.")
}