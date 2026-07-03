This is a list of Win32 API dlls that should be accessed via [Microsoft.Windows.CsWin32](https://github.com/microsoft/CsWin32) instead of via `[DllImport(...)]` and `[LibraryImport(...)]`

### Core Win32 / OS services

| DLL              | Typical use                                                                                                                                                                                        |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `kernel32.dll`   | Processes, threads, files, console, synchronization, memory, environment variables, DLL loading. Examples: `CreateFileW`, `CreateProcessW`, `CreateThread`, `WaitForSingleObject`, `LoadLibraryW`. |
| `kernelbase.dll` | Modern implementation host for many base APIs. Often functions imported from `kernel32.dll` are forwarded here. Usually you still link against `kernel32.lib` / call `kernel32.dll`.               |
| `ntdll.dll`      | Native NT API layer: `Nt*`, `Zw*`, `Rtl*`, loader internals. Important for systems work, debugging, malware analysis, syscall research. Not usually used directly in normal application code.      |
| `advapi32.dll`   | Registry, Windows services, security descriptors, access tokens, event log, LSA-ish APIs. Examples: `RegOpenKeyExW`, `OpenProcessToken`, `StartServiceW`.                                          |
| `secur32.dll`    | SSPI authentication/security packages. Used for Windows authentication, Kerberos/NTLM, credential negotiation.                                                                                     |
| `bcrypt.dll`     | CNG cryptography: hashing, encryption, key handling. Modern replacement for many older crypto APIs.                                                                                                |
| `crypt32.dll`    | Certificates, certificate stores, encoding/decoding, chain validation.                                                                                                                             |
| `version.dll`    | File version resource access. Example: `GetFileVersionInfoW`.                                                                                                                                      |
| `psapi.dll`      | Process/module enumeration and process memory information. Often used by diagnostic tools.                                                                                                         |
| `dbghelp.dll`    | Symbols, stack walking, minidumps. Examples: `SymInitialize`, `StackWalk64`, `MiniDumpWriteDump`.                                                                                                  |
| `powrprof.dll`   | Power profiles, sleep/hibernate/battery information.                                                                                                                                               |
| `wintrust.dll`   | Authenticode and trust verification. Example: `WinVerifyTrust`.                                                                                                                                    |

Microsoft’s “System Services” area covers many of the traditional OS-level APIs such as file system, processes, memory, synchronization, services, and related infrastructure. ([Microsoft Learn][2])

### Windowing, UI, graphics

| DLL            | Typical use                                                                                                                                                                            |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `user32.dll`   | Windows, messages, input, keyboard/mouse, clipboard, menus, dialogs, window stations/desktops, hooks. Examples: `CreateWindowExW`, `SendMessageW`, `GetMessageW`, `SetWindowLongPtrW`. |
| `gdi32.dll`    | Classic GDI 2D drawing, fonts, pens, brushes, bitmaps, printer/device contexts. Examples: `CreateFontW`, `BitBlt`, `TextOutW`, `CreateCompatibleDC`.                                   |
| `comctl32.dll` | Common controls: ListView, TreeView, ProgressBar, Toolbar, StatusBar, etc.                                                                                                             |
| `comdlg32.dll` | Common dialogs: file open/save, color picker, font picker, print dialog.                                                                                                               |
| `shell32.dll`  | Windows Shell integration: file operations, special folders, ShellExecute, known folders, tray icons, shell links.                                                                     |
| `shlwapi.dll`  | Shell lightweight utility APIs: path/string helpers, URL helpers, registry helpers.                                                                                                    |
| `dwmapi.dll`   | Desktop Window Manager integration: glass/frame attributes, thumbnails, composition info.                                                                                              |
| `uxtheme.dll`  | Visual styles/theming for classic Win32 controls.                                                                                                                                      |
| `imm32.dll`    | Input Method Editor support, relevant for East Asian text input.                                                                                                                       |
| `winmm.dll`    | Older multimedia APIs: timers, wave audio, joystick, MCI. Still seen in legacy/native code.                                                                                            |
| `msimg32.dll`  | AlphaBlend, GradientFill, transparent blits.                                                                                                                                           |
| `gdiplus.dll`  | GDI+ drawing, images, anti-aliased 2D graphics. Higher-level than raw GDI.                                                                                                             |

`user32.dll` corresponds to the classic user/windowing API area, while GDI is Microsoft’s classic 2D graphics/device-context system for displays and printers. ([Microsoft Learn][3])

### COM, OLE, automation

| DLL            | Typical use                                                                   |
| -------------- | ----------------------------------------------------------------------------- |
| `ole32.dll`    | Core COM: `CoInitializeEx`, `CoCreateInstance`, monikers, structured storage. |
| `oleaut32.dll` | OLE Automation: `VARIANT`, `BSTR`, `IDispatch`, type libraries.               |
| `uuid.dll`     | Provides GUID/IID/CLSID symbols when linking native code.                     |
| `propsys.dll`  | Windows property system, used by Shell metadata and structured properties.    |
| `actxprxy.dll` | ActiveX proxy/stub support. Mostly legacy/COM infrastructure.                 |

### Networking and internet

| DLL            | Typical use                                                                                              |
| -------------- | -------------------------------------------------------------------------------------------------------- |
| `ws2_32.dll`   | Winsock 2 sockets: TCP/UDP, `socket`, `connect`, `send`, `recv`, `select`, etc.                          |
| `iphlpapi.dll` | IP helper APIs: adapters, routes, IP statistics, network tables.                                         |
| `dnsapi.dll`   | DNS queries and resolver APIs.                                                                           |
| `wininet.dll`  | High-level HTTP/FTP APIs historically used by client apps; Internet Explorer settings/proxy integration. |
| `winhttp.dll`  | HTTP client API more suitable for services/server-side components than `wininet.dll`.                    |
| `wlanapi.dll`  | Wi-Fi profile and interface management.                                                                  |
| `netapi32.dll` | Windows networking/admin APIs: users, groups, shares, servers, domains.                                  |
| `mpr.dll`      | Multiple Provider Router: mapped network drives, network resources.                                      |
| `rasapi32.dll` | Remote Access Service / VPN / dial-up APIs. Mostly legacy but still exists.                              |

### File system, storage, setup, devices

| DLL            | Typical use                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------ |
| `setupapi.dll` | Device installation, device interfaces, INF/setup class APIs. Very common for USB/HID/driver-adjacent tools. |
| `cfgmgr32.dll` | Configuration Manager device tree APIs: enumerate devices, query device properties.                          |
| `hid.dll`      | HID device APIs: parse HID reports, get preparsed data, capabilities.                                        |
| `winusb.dll`   | User-mode access to USB devices using WinUSB driver.                                                         |
| `newdev.dll`   | Device installation helper functions.                                                                        |
| `virtdisk.dll` | VHD/VHDX virtual disk APIs.                                                                                  |
| `cabinet.dll`  | CAB archive compression/decompression.                                                                       |
| `imagehlp.dll` | PE image helper APIs; older sibling/relative of `dbghelp.dll`.                                               |
| `mpr.dll`      | Also relevant here for network drive connections.                                                            |

### DirectX / modern rendering / media-adjacent

| DLL                 | Typical use                                                                |
| ------------------- | -------------------------------------------------------------------------- |
| `d3d11.dll`         | Direct3D 11 rendering.                                                     |
| `d3d12.dll`         | Direct3D 12 rendering.                                                     |
| `dxgi.dll`          | DXGI swap chains, adapters, displays, presentation.                        |
| `d2d1.dll`          | Direct2D 2D rendering.                                                     |
| `dwrite.dll`        | DirectWrite text layout and font rendering.                                |
| `windowscodecs.dll` | WIC image codecs: PNG, JPEG, TIFF, BMP, metadata, pixel format conversion. |
| `mfplat.dll`        | Media Foundation platform.                                                 |
| `mf.dll`            | Media Foundation core.                                                     |
| `mfreadwrite.dll`   | Media Foundation source reader/sink writer APIs.                           |
| `xaudio2_9.dll`     | XAudio2 audio engine on modern Windows.                                    |
| `xinput1_4.dll`     | Xbox-compatible controller input.                                          |

### Runtime and support DLLs often seen next to Win32 code

| DLL                                       | Typical use                                                                                                   |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `ucrtbase.dll`                            | Universal C Runtime: C library functions used by Visual C++ programs. Not “Win32 API” proper, but ubiquitous. |
| `msvcrt.dll`                              | Older Microsoft C runtime DLL. Still present, but not what modern Visual C++ normally targets directly.       |
| `vcruntime140.dll` / `vcruntime140_1.dll` | Visual C++ runtime support. Deployed with many native apps.                                                   |
| `mscoree.dll`                             | .NET CLR hosting bootstrap DLL. Seen in .NET Framework executables and mixed environments.                    |

### Special note: `api-ms-win-*.dll` and `ext-ms-win-*.dll`

On modern Windows you will often see imports such as:

| Name pattern                | Meaning                                           |
| --------------------------- | ------------------------------------------------- |
| `api-ms-win-core-*.dll`     | API-set contract names for core Windows APIs.     |
| `api-ms-win-security-*.dll` | API-set contract names for security-related APIs. |
| `ext-ms-win-*.dll`          | Extension API-set contracts.                      |
