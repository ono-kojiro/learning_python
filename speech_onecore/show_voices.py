import win32com.client
cat  = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
cat.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)
for token in cat.EnumerateTokens():
    print(token.GetDescription())
