# 🎯 Strato DNS - Si të Heqësh IPv6 (AAAA Records)

## Hapi 1: Hyrja në Strato Customer Service

1. Shko te: **https://www.strato.de/apps/CustomerService**
2. Login me kredencialet e tua
3. Nëse nuk e di password-in: "Passwort vergessen?"

## Hapi 2: Gjej Domain Management

1. Dashboard → **Pakete & Domains** (ose "Packages & Domains")
2. Gjej: **clisonix.com**
3. Kliko: **Verwalten** (Manage) ose **DNS Einstellungen** (DNS Settings)

## Hapi 3: DNS Records Management

Duhet të shohësh diçka si kjo:

\\\
Type    Name                    Value
────────────────────────────────────────────────────────
A       clisonix.com            157.90.234.158        ← MBAJE
AAAA    clisonix.com            2a01:4f8:c0c:a9fb::1  ← FSHIJE
CNAME   www.clisonix.com        clisonix.com          ← MBAJE
\\\

## Hapi 4: Fshij AAAA Records

### Për clisonix.com:
1. Gjej rreshtin: **AAAA | clisonix.com | 2a01:4f8:c0c:a9fb::1**
2. Kliko: **Löschen** (Delete) ose **❌** (X icon)
3. Konfirmo: **Ja** (Yes)

### Për www.clisonix.com (nëse ka):
1. Gjej rreshtin: **AAAA | www.clisonix.com | ...**
2. Kliko: **Löschen** (Delete)
3. Konfirmo: **Ja**

## Hapi 5: Ruaj Ndryshimet

1. Kliko: **Speichern** (Save) ose **Änderungen übernehmen** (Apply Changes)
2. Konfirmo nëse pyet
3. Prit popup: "Änderungen gespeichert" (Changes saved)

## Hapi 6: Verifikimi Final

### Para se të dalësh nga Strato:

Kontrollo që ke VETËM këto:

\\\
✅ A     clisonix.com          157.90.234.158
✅ CNAME www.clisonix.com      clisonix.com

❌ AAAA  (NOTHING - should be DELETED)
\\\

---

## 🕐 Sa Kohë Duhet?

| Veprim                  | Kohë          |
|-------------------------|---------------|
| Login & Navigate        | 1-2 min       |
| Delete AAAA Records     | 30 sec        |
| Save Changes            | 10 sec        |
| **DNS Propagation**     | **5-10 min**  |
| **Total**               | **~15 min**   |

---

## ✅ Si të Testosh (Pas 10 Minutave)

### Në PowerShell:

\\\powershell
# Test 1: DNS Lookup
nslookup www.clisonix.com

# Duhet të shohësh VETËM:
# - CNAME: clisonix.com
# - A: 157.90.234.158
# - NO AAAA!

# Test 2: Run automated script
.\test-dns-ipv4.ps1
\\\

### Në Browser:

1. Open **Incognito/Private window** (të shmangësh cache)
2. Shko te: **https://www.clisonix.com**
3. Duhet të hapet INSTANTLY pa timeout ✅

---

## 🆘 Nëse Nuk Gjen "Löschen" (Delete)

### Opsioni Alternativ: Modifiko në tekst

Disa versione të Strato kanë "Advanced DNS Editor":

1. Kliko: **Experten-Modus** (Expert Mode) ose **Zone File**
2. Gjej rreshtin me: \AAAA\
3. Fshije tërë rreshtin
4. Save

---

## 📸 Screenshots Locations (ku të gjesh çdo gjë)

### Dashboard:
\\\
Strato Kunden-Login
  └─ Übersicht (Overview)
      └─ Pakete & Domains
          └─ clisonix.com [Verwalten]
\\\

### DNS Settings:
\\\
clisonix.com Management
  └─ DNS Einstellungen (DNS Settings)
      └─ DNS Records Tabelle
          ├─ A Records       ← MBAJE
          ├─ AAAA Records    ← FSHIJE
          └─ CNAME Records   ← MBAJE
\\\

---

## 🎯 Çfarë NUK Duhet të Prekësh

### MOS FSHI KËTO:

❌ **A Record** (157.90.234.158) ← Kjo është IP e serverit tënd!
❌ **CNAME Record** (www → clisonix.com) ← Kjo redirect-on www
❌ **MX Records** (nëse ke email)
❌ **TXT Records** (nëse ke SPF/DKIM)

### FSHI VETËM KËTO:

✅ **AAAA Records** (IPv6) ← VETËM KËTO!

---

## 🔧 Troubleshooting

### "Nuk gjej DNS Settings"
→ Provo: Pakete → Domain → Einstellungen → DNS-Verwaltung

### "Button 'Löschen' disabled"
→ Shiko nëse ke "Expert Mode" ose "Edit Zone"

### "Ndryshimet nuk ruhen"
→ Refresh page dhe provo përsëri

### "AAAA perseri shfaqet"
→ Kontrollo Cloudflare nëse përdor (Proxy OFF për test)

---

## 📞 Strato Support (nëse ngec)

- **Telefon:** +49 30 300 146 0
- **Email:** support@strato.de
- **Thuaj:** "Ich möchte die AAAA Records für clisonix.com löschen"
  (Dua të fshij AAAA records për clisonix.com)

---

## 🎉 Pas Suksesit

Kur www.clisonix.com hapet në browser:

1. ✅ AAAA records hequr
2. ✅ IPv4-only DNS
3. ✅ Zero timeout
4. ✅ Website LIVE!

Më thuaj: "DONE! www hapet!" dhe kalojmë te next phase 🚀

---

**Last Updated:** December 26, 2025
**Estimated Time:** 15 minutes total (include propagation)
