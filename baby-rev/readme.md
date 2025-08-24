# Excel Macro Analysis

Writeup untuk CTF challenge forensik yang melibatkan analisis VBA Macro dalam file Excel.

## Challenge

Diberikan file `gemastik.xls` yang perlu dianalisis untuk mendapatkan flag tersembunyi.

## Analisis

### 1. Identifikasi File

File `gemastik.xls` adalah **Excel 97–2003 (OLE Compound File)** yang biasanya berisi VBA Macro.

```bash
file gemastik.xls
# Output: gemastik.xls: Microsoft Excel 97-2003 Worksheet
```

### 2. Ekstraksi Macro

Menggunakan `oletools` untuk menganalisis struktur OLE:

```bash
pip install oletools
olevba gemastik.xls -a
```

Hasilnya menunjukkan stream:
```
['_VBA_PROJECT_CUR', 'VBA', 'ThisWorkbook']
['_VBA_PROJECT_CUR', 'VBA', 'Sheet1']
```

### 3. Dump Binary Stream

Manual dump stream `ThisWorkbook` yang berisi macro:

```python
import olefile

ole = olefile.OleFileIO('gemastik.xls')
with ole.open('_VBA_PROJECT_CUR/VBA/ThisWorkbook') as f:
    data = f.read()

# Tulis ke file untuk analisis
with open('dump.bin', 'wb') as f:
    f.write(data)
```

### 4. Analisis Hasil Dump

Di dalam dump binary, ditemukan pattern seperti:
```
kg$(e$(m$(a$(s$(t$(i$(k$({$(1$(_$(4$(m$(_$(s$(t$(0$(m$(p$(e$(d$(_$(_$(_$(_$(h$(m$(m$(m$(}$(
```

### 5. Ekstraksi Flag

Bersihkan pattern dengan menghilangkan `$(` separator:

```python
raw = "kg$(e$(m$(a$(s$(t$(i$(k$({$(1$(_$(4$(m$(_$(s$(t$(0$(m$(p$(e$(d$(_$(_$(_$(_$(h$(m$(m$(m$(}$("

# Ambil karakter sebelum '$('
parts = raw.split("$(")
flag = ''.join([part[0] if len(part) > 0 else '' for part in parts])
print(flag)
```

### 6. Verifikasi

Di macro juga ada fungsi `checkflag()`:
```vba
Sub checkflag()
    If Range("A1").Value = "[REDACTED]" Then
        MsgBox "Correct!"
    Else
        MsgBox "Incorrect!"
    End If
End Sub
```

## Tools

```bash
# Analisis otomatis
olevba gemastik.xls --decode

# Atau cari string langsung
strings gemastik.xls | grep -i flag_format
```

## Flag

```
flag_format{[REDACTED]}
```
