"""
AntiDetect Core - Fingerprint Generation & Injection
AntiDetect Fingerprint by juldeptrai

Provides:
- generate_fingerprint(): Generate random browser fingerprint
- get_inject_script(fingerprint, profile_name, watermark_style): Get JS injection script
"""

import random
import platform
import os


# Common screen resolutions
RESOLUTIONS = [
    {"w": 1920, "h": 1080},
    {"w": 2560, "h": 1440},
    {"w": 1366, "h": 768},
    {"w": 1536, "h": 864},
    {"w": 1440, "h": 900},
]

# Common WebGL renderers (fake GPU info)
WEBGL_RENDERERS = [
    {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) Iris Xe Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD, AMD Radeon RX 580 Series Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
]


def generate_fingerprint(
    timezone: str = "America/Los_Angeles",
    language: str = "en-US",
    geolocation: dict = None,
    screen_width: int = None,
    screen_height: int = None,
    webgl_spoof: bool = True,  # Set False to avoid Pixelscan masking detection
) -> dict:
    """
    Generate a randomized browser fingerprint.
    
    Args:
        webgl_spoof: If True, spoof WebGL vendor/renderer (may trigger masking detection)
                     If False, use real GPU (no masking but reveals hardware)
    
    Args:
        timezone: IANA timezone string (e.g., "America/New_York")
        language: Browser language (e.g., "en-US")
        geolocation: Optional dict with 'latitude', 'longitude', 'accuracy'
        screen_width: Optional custom screen width
        screen_height: Optional custom screen height
    
    Returns:
        dict: Fingerprint data for injection
    """
    # Detect host platform
    system = platform.system().lower()
    if system == "windows":
        plat = "Win32"
    elif system == "darwin":
        plat = "MacIntel"
    else:
        plat = "Linux x86_64"
    
    # Random resolution or custom
    if screen_width and screen_height:
        res = {"w": screen_width, "h": screen_height}
    else:
        res = random.choice(RESOLUTIONS)
    
    # Languages array
    lang_base = language.split("-")[0] if "-" in language else language
    languages = [language, lang_base]
    
    # Canvas noise (subtle random offsets)
    canvas_noise = {
        "r": random.randint(-5, 5),
        "g": random.randint(-5, 5),
        "b": random.randint(-5, 5),
        "a": random.randint(-5, 5),
    }
    
    fingerprint = {
        "platform": plat,
        "screen": {"width": res["w"], "height": res["h"]},
        "window": {"width": res["w"], "height": res["h"]},
        "languages": languages,
        "language": language,
        "hardwareConcurrency": random.choice([4, 8, 12, 16]),
        "deviceMemory": random.choice([2, 4, 8]),
        "canvasNoise": canvas_noise,
        "audioNoise": random.random() * 0.000001,
        "noiseSeed": random.randint(0, 9999999),
        "timezone": timezone,
    }
    
    # Add WebGL spoofing only if enabled
    if webgl_spoof:
        webgl_info = random.choice(WEBGL_RENDERERS)
        fingerprint["webgl"] = {
            "vendor": webgl_info["vendor"],
            "renderer": webgl_info["renderer"],
        }
    
    # Add geolocation if provided
    if geolocation:
        fingerprint["geolocation"] = geolocation
    
    return fingerprint


def get_inject_script(
    fingerprint: dict,
    profile_name: str = "Profile",
    watermark_style: str = "enhanced"
) -> str:
    """
    Generate the JavaScript injection script for fingerprint spoofing.
    
    Args:
        fingerprint: Fingerprint dict from generate_fingerprint()
        profile_name: Name to display in watermark
        watermark_style: 'enhanced' (bottom-right) or 'banner' (top bar)
    
    Returns:
        str: JavaScript code to inject via add_init_script()
    """
    import json
    
    fp_json = json.dumps(fingerprint)
    safe_profile_name = profile_name.replace("<", "").replace(">", "").replace("\"", "").replace("'", "").replace("&", "")
    style = watermark_style or "enhanced"
    
    return f'''
(function() {{
    try {{
        const fp = {fp_json};
        const targetTimezone = fp.timezone || "America/Los_Angeles";

        // --- Global Helper: makeNative ---
        // Makes hooked functions appear as native code to avoid detection
        const makeNative = (func, name) => {{
            const nativeStr = 'function ' + name + '() {{ [native code] }}';
            Object.defineProperty(func, 'toString', {{
                value: function() {{ return nativeStr; }},
                configurable: true,
                writable: true
            }});
            Object.defineProperty(func.toString, 'toString', {{
                value: function() {{ return 'function toString() {{ [native code] }}'; }},
                configurable: true,
                writable: true
            }});
            if (func.prototype) {{
                Object.defineProperty(func.prototype.constructor, 'toString', {{
                    value: function() {{ return nativeStr; }},
                    configurable: true,
                    writable: true
                }});
            }}
            return func;
        }};

        // --- 0. Stealth Timezone Hook (Windows Only) ---
        const isWindows = navigator.platform && navigator.platform.toLowerCase().includes('win');
        if (isWindows && fp.timezone && fp.timezone !== 'Auto') {{
            const tzMakeNative = (func, name) => {{
                const nativeStr = 'function ' + name + '() {{ [native code] }}';
                func.toString = function() {{ return nativeStr; }};
                func.toString.toString = function() {{ return 'function toString() {{ [native code] }}'; }};
                return func;
            }};

            const getTimezoneOffsetForZone = (tz) => {{
                try {{
                    const now = new Date();
                    const utcDate = new Date(now.toLocaleString('en-US', {{ timeZone: 'UTC' }}));
                    const tzDate = new Date(now.toLocaleString('en-US', {{ timeZone: tz }}));
                    return Math.round((utcDate - tzDate) / 60000);
                }} catch (e) {{
                    return new Date().getTimezoneOffset();
                }}
            }};

            const targetOffset = getTimezoneOffsetForZone(targetTimezone);

            // Hook Date.prototype.getTimezoneOffset
            const origGetTimezoneOffset = Date.prototype.getTimezoneOffset;
            Date.prototype.getTimezoneOffset = tzMakeNative(function getTimezoneOffset() {{
                return targetOffset;
            }}, 'getTimezoneOffset');

            // Hook Intl.DateTimeFormat.prototype.resolvedOptions
            const OrigDTFProto = Intl.DateTimeFormat.prototype;
            const origResolvedOptions = OrigDTFProto.resolvedOptions;
            OrigDTFProto.resolvedOptions = tzMakeNative(function resolvedOptions() {{
                const result = origResolvedOptions.call(this);
                result.timeZone = targetTimezone;
                return result;
            }}, 'resolvedOptions');

            // Hook Date.prototype.toLocaleString family
            const dateMethodsToHook = ['toLocaleString', 'toLocaleDateString', 'toLocaleTimeString'];
            dateMethodsToHook.forEach(methodName => {{
                const origMethod = Date.prototype[methodName];
                Date.prototype[methodName] = tzMakeNative(function(...args) {{
                    if (args.length === 0) {{
                        return origMethod.call(this, undefined, {{ timeZone: targetTimezone }});
                    }} else if (args.length === 1) {{
                        return origMethod.call(this, args[0], {{ timeZone: targetTimezone }});
                    }} else {{
                        const opts = args[1] || {{}};
                        if (!opts.timeZone) {{
                            opts.timeZone = targetTimezone;
                        }}
                        return origMethod.call(this, args[0], opts);
                    }}
                }}, methodName);
            }});

            // Hook new Intl.DateTimeFormat() constructor
            const OrigDateTimeFormat = Intl.DateTimeFormat;
            Intl.DateTimeFormat = function(locales, options) {{
                const opts = options ? {{ ...options }} : {{}};
                if (!opts.timeZone) {{
                    opts.timeZone = targetTimezone;
                }}
                return new OrigDateTimeFormat(locales, opts);
            }};
            Intl.DateTimeFormat.prototype = OrigDateTimeFormat.prototype;
            Intl.DateTimeFormat.supportedLocalesOf = OrigDateTimeFormat.supportedLocalesOf.bind(OrigDateTimeFormat);
            tzMakeNative(Intl.DateTimeFormat, 'DateTimeFormat');
        }}

        // --- 1. Remove WebDriver & Puppeteer detection ---
        if (navigator.webdriver) {{
            Object.defineProperty(navigator, 'webdriver', {{ get: () => false }});
        }}
        
        // Remove cdc_ variables (Puppeteer/Selenium markers)
        const cdcRegex = /cdc_[a-zA-Z0-9]+/;
        for (const key in window) {{
            if (cdcRegex.test(key)) {{
                delete window[key];
            }}
        }}
        
        // Remove common automation variables
        ['$cdc_asdjflasutopfhvcZLmcfl_', '$chrome_asyncScriptInfo', 'callPhantom', 'webdriver'].forEach(k => {{
            if (window[k]) delete window[k];
        }});
        
        Object.defineProperty(window, 'chrome', {{
            writable: true,
            enumerable: true,
            configurable: false,
            value: {{ 
                app: {{ 
                    isInstalled: false, 
                    InstallState: {{ DISABLED: 'disabled', INSTALLED: 'installed', NOT_INSTALLED: 'not_installed' }}, 
                    RunningState: {{ CANNOT_RUN: 'cannot_run', READY_TO_RUN: 'ready_to_run', RUNNING: 'running' }} 
                }}, 
                runtime: {{ 
                    OnInstalledReason: {{ CHROME_UPDATE: 'chrome_update', INSTALL: 'install', SHARED_MODULE_UPDATE: 'shared_module_update', UPDATE: 'update' }}, 
                    OnRestartRequiredReason: {{ APP_UPDATE: 'app_update', OS_UPDATE: 'os_update', PERIODIC: 'periodic' }}, 
                    PlatformArch: {{ ARM: 'arm', ARM64: 'arm64', MIPS: 'mips', MIPS64: 'mips64', X86_32: 'x86-32', X86_64: 'x86-64' }}, 
                    PlatformNaclArch: {{ ARM: 'arm', MIPS: 'mips', X86_32: 'x86-32', X86_64: 'x86-64' }}, 
                    PlatformOs: {{ ANDROID: 'android', CROS: 'cros', LINUX: 'linux', MAC: 'mac', OPENBSD: 'openbsd', WIN: 'win' }}, 
                    RequestUpdateCheckStatus: {{ NO_UPDATE: 'no_update', THROTTLED: 'throttled', UPDATE_AVAILABLE: 'update_available' }} 
                }} 
            }}
        }});

        // --- 1.5 Screen Resolution Hook ---
        if (fp.screen && fp.screen.width && fp.screen.height) {{
            const screenWidth = fp.screen.width;
            const screenHeight = fp.screen.height;
            
            Object.defineProperty(screen, 'width', {{
                get: makeNative(function width() {{ return screenWidth; }}, 'width'),
                configurable: true
            }});
            Object.defineProperty(screen, 'height', {{
                get: makeNative(function height() {{ return screenHeight; }}, 'height'),
                configurable: true
            }});
            Object.defineProperty(screen, 'availWidth', {{
                get: makeNative(function availWidth() {{ return screenWidth; }}, 'availWidth'),
                configurable: true
            }});
            Object.defineProperty(screen, 'availHeight', {{
                get: makeNative(function availHeight() {{ return screenHeight - 40; }}, 'availHeight'),
                configurable: true
            }});
            Object.defineProperty(window, 'outerWidth', {{
                get: makeNative(function outerWidth() {{ return screenWidth; }}, 'outerWidth'),
                configurable: true
            }});
            Object.defineProperty(window, 'outerHeight', {{
                get: makeNative(function outerHeight() {{ return screenHeight; }}, 'outerHeight'),
                configurable: true
            }});
        }}

        // --- 1.6 Stealthy Hardware Fingerprint Hook (CPU Cores & Memory) ---
        if (fp.hardwareConcurrency) {{
            const targetCores = fp.hardwareConcurrency;
            const coresGetter = function() {{ return targetCores; }};
            Object.defineProperty(coresGetter, 'toString', {{
                value: function() {{ return 'function get hardwareConcurrency() {{ [native code] }}'; }},
                configurable: true, writable: true
            }});
            Object.defineProperty(Navigator.prototype, 'hardwareConcurrency', {{
                get: coresGetter,
                configurable: true
            }});
        }}
        
        if (fp.deviceMemory) {{
            const targetMemory = fp.deviceMemory;
            const memoryGetter = function() {{ return targetMemory; }};
            Object.defineProperty(memoryGetter, 'toString', {{
                value: function() {{ return 'function get deviceMemory() {{ [native code] }}'; }},
                configurable: true, writable: true
            }});
            Object.defineProperty(Navigator.prototype, 'deviceMemory', {{
                get: memoryGetter,
                configurable: true
            }});
        }}

        // --- 2. Stealth Geolocation Hook ---
        if (fp.geolocation) {{
            const {{ latitude, longitude }} = fp.geolocation;
            const accuracy = 500 + Math.floor(Math.random() * 1000);

            const geoMakeNative = (func, name) => {{
                Object.defineProperty(func, 'toString', {{
                    value: function() {{ return "function " + name + "() {{ [native code] }}"; }},
                    configurable: true,
                    writable: true
                }});
                Object.defineProperty(func.toString, 'toString', {{
                    value: function() {{ return "function toString() {{ [native code] }}"; }},
                    configurable: true,
                    writable: true
                }});
                return func;
            }};

            const fakeGetCurrentPosition = function getCurrentPosition(success, error, options) {{
                const position = {{
                    coords: {{
                        latitude: latitude + (Math.random() - 0.5) * 0.005,
                        longitude: longitude + (Math.random() - 0.5) * 0.005,
                        accuracy: accuracy,
                        altitude: null,
                        altitudeAccuracy: null,
                        heading: null,
                        speed: null
                    }},
                    timestamp: Date.now()
                }};
                setTimeout(() => success(position), 10);
            }};

            const fakeWatchPosition = function watchPosition(success, error, options) {{
                fakeGetCurrentPosition(success, error, options);
                return Math.floor(Math.random() * 10000) + 1;
            }};

            Object.defineProperty(Geolocation.prototype, 'getCurrentPosition', {{
                value: geoMakeNative(fakeGetCurrentPosition, 'getCurrentPosition'),
                configurable: true,
                writable: true
            }});

            Object.defineProperty(Geolocation.prototype, 'watchPosition', {{
                value: geoMakeNative(fakeWatchPosition, 'watchPosition'),
                configurable: true,
                writable: true
            }});
        }}

        // --- 2.5 Intl API Language Override ---
        if (fp.language && fp.language !== 'auto') {{
            const targetLang = fp.language;
            
            const OrigDTF = Intl.DateTimeFormat;
            const OrigNF = Intl.NumberFormat;
            const OrigColl = Intl.Collator;
            
            const hookedDTF = function DateTimeFormat(locales, options) {{
                return new OrigDTF(locales || targetLang, options);
            }};
            hookedDTF.prototype = OrigDTF.prototype;
            hookedDTF.supportedLocalesOf = OrigDTF.supportedLocalesOf.bind(OrigDTF);
            Intl.DateTimeFormat = makeNative(hookedDTF, 'DateTimeFormat');
            
            const hookedNF = function NumberFormat(locales, options) {{
                return new OrigNF(locales || targetLang, options);
            }};
            hookedNF.prototype = OrigNF.prototype;
            hookedNF.supportedLocalesOf = OrigNF.supportedLocalesOf.bind(OrigNF);
            Intl.NumberFormat = makeNative(hookedNF, 'NumberFormat');
            
            const hookedColl = function Collator(locales, options) {{
                return new OrigColl(locales || targetLang, options);
            }};
            hookedColl.prototype = OrigColl.prototype;
            hookedColl.supportedLocalesOf = OrigColl.supportedLocalesOf.bind(OrigColl);
            Intl.Collator = makeNative(hookedColl, 'Collator');
        }}

        // --- 3. Canvas Noise ---
        const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
        const hookedGetImageData = function getImageData(x, y, w, h) {{
            const imageData = originalGetImageData.apply(this, arguments);
            if (fp.noiseSeed) {{
                for (let i = 0; i < imageData.data.length; i += 4) {{
                    if ((i + fp.noiseSeed) % 53 === 0) {{
                        const noise = fp.canvasNoise ? (fp.canvasNoise.a || 0) : 0;
                        imageData.data[i+3] = Math.max(0, Math.min(255, imageData.data[i+3] + noise));
                    }}
                }}
            }}
            return imageData;
        }};
        CanvasRenderingContext2D.prototype.getImageData = makeNative(hookedGetImageData, 'getImageData');

        // --- 4. Audio Noise ---
        const originalGetChannelData = AudioBuffer.prototype.getChannelData;
        const hookedGetChannelData = function getChannelData(channel) {{
            const results = originalGetChannelData.apply(this, arguments);
            const noise = fp.audioNoise || 0.0000001;
            for (let i = 0; i < 100 && i < results.length; i++) {{
                results[i] = results[i] + noise;
            }}
            return results;
        }};
        AudioBuffer.prototype.getChannelData = makeNative(hookedGetChannelData, 'getChannelData');

        // --- 5. WebRTC Protection ---
        const originalPC = window.RTCPeerConnection;
        const hookedPC = function RTCPeerConnection(config) {{
            if(!config) config = {{}};
            config.iceTransportPolicy = 'relay'; 
            return new originalPC(config);
        }};
        hookedPC.prototype = originalPC.prototype;
        window.RTCPeerConnection = makeNative(hookedPC, 'RTCPeerConnection');

        // --- 5.5 WebGL Spoofing with Noise ---
        if (fp.webgl && fp.webgl.vendor && fp.webgl.renderer) {{
            const fakeVendor = fp.webgl.vendor;
            const fakeRenderer = fp.webgl.renderer;
            const webglNoiseSeed = fp.noiseSeed || Math.random() * 1000000;
            
            // Get debug extension constants
            const UNMASKED_VENDOR_WEBGL = 0x9245;
            const UNMASKED_RENDERER_WEBGL = 0x9246;
            
            // Hook WebGLRenderingContext.getParameter
            const origGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = makeNative(function getParameter(param) {{
                if (param === UNMASKED_VENDOR_WEBGL) return fakeVendor;
                if (param === UNMASKED_RENDERER_WEBGL) return fakeRenderer;
                return origGetParameter.call(this, param);
            }}, 'getParameter');
            
            // Hook WebGL2RenderingContext.getParameter if available
            if (typeof WebGL2RenderingContext !== 'undefined') {{
                const origGetParameter2 = WebGL2RenderingContext.prototype.getParameter;
                WebGL2RenderingContext.prototype.getParameter = makeNative(function getParameter(param) {{
                    if (param === UNMASKED_VENDOR_WEBGL) return fakeVendor;
                    if (param === UNMASKED_RENDERER_WEBGL) return fakeRenderer;
                    return origGetParameter2.call(this, param);
                }}, 'getParameter');
            }}
            
            // Hook readPixels to add noise (changes WebGL hash)
            const origReadPixels = WebGLRenderingContext.prototype.readPixels;
            WebGLRenderingContext.prototype.readPixels = makeNative(function readPixels(...args) {{
                origReadPixels.apply(this, args);
                const pixels = args[6];
                if (pixels && pixels.length) {{
                    for (let i = 0; i < pixels.length; i += 4) {{
                        if ((i + webglNoiseSeed) % 97 === 0) {{
                            pixels[i] = Math.max(0, Math.min(255, pixels[i] + (webglNoiseSeed % 3) - 1));
                        }}
                    }}
                }}
            }}, 'readPixels');
            
            if (typeof WebGL2RenderingContext !== 'undefined') {{
                const origReadPixels2 = WebGL2RenderingContext.prototype.readPixels;
                WebGL2RenderingContext.prototype.readPixels = makeNative(function readPixels(...args) {{
                    origReadPixels2.apply(this, args);
                    const pixels = args[6];
                    if (pixels && pixels.length) {{
                        for (let i = 0; i < pixels.length; i += 4) {{
                            if ((i + webglNoiseSeed) % 97 === 0) {{
                                pixels[i] = Math.max(0, Math.min(255, pixels[i] + (webglNoiseSeed % 3) - 1));
                            }}
                        }}
                    }}
                }}, 'readPixels');
            }}
            
            // Hook canvas toDataURL for WebGL canvas
            const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = makeNative(function toDataURL(type, quality) {{
                const ctx = this.getContext('webgl') || this.getContext('webgl2') || this.getContext('experimental-webgl');
                if (ctx) {{
                    // Add subtle noise to WebGL canvas before export
                    const ctx2d = document.createElement('canvas').getContext('2d');
                    if (ctx2d) {{
                        ctx2d.canvas.width = this.width;
                        ctx2d.canvas.height = this.height;
                        ctx2d.drawImage(this, 0, 0);
                        const imageData = ctx2d.getImageData(0, 0, this.width, this.height);
                        for (let i = 0; i < imageData.data.length; i += 4) {{
                            if ((i + webglNoiseSeed) % 101 === 0) {{
                                imageData.data[i] = Math.max(0, Math.min(255, imageData.data[i] + (webglNoiseSeed % 5) - 2));
                            }}
                        }}
                        ctx2d.putImageData(imageData, 0, 0);
                        return origToDataURL.call(ctx2d.canvas, type, quality);
                    }}
                }}
                return origToDataURL.call(this, type, quality);
            }}, 'toDataURL');
        }}

        // --- 6. Watermark (Profile Name Display) ---
        const watermarkStyle = '{style}';
        
        function createWatermark() {{
            try {{
                if (document.getElementById('juldeptrai-watermark')) return;
                
                if (!document.body) {{
                    setTimeout(createWatermark, 50);
                    return;
                }}
                
                if (watermarkStyle === 'banner') {{
                    const banner = document.createElement('div');
                    banner.id = 'juldeptrai-watermark';
                    banner.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; background: linear-gradient(135deg, rgba(102, 126, 234, 0.5), rgba(118, 75, 162, 0.5)); backdrop-filter: blur(10px); color: white; padding: 5px 20px; text-align: center; font-size: 12px; font-weight: 500; z-index: 2147483647; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: flex; align-items: center; justify-content: center; gap: 8px; font-family: monospace;';
                    
                    const icon = document.createElement('span');
                    icon.textContent = '🔹';
                    icon.style.cssText = 'font-size: 14px;';
                    
                    const text = document.createElement('span');
                    text.textContent = 'Profile: {safe_profile_name}';
                    
                    const closeBtn = document.createElement('button');
                    closeBtn.textContent = '×';
                    closeBtn.style.cssText = 'position: absolute; right: 10px; background: rgba(255,255,255,0.2); border: none; color: white; width: 20px; height: 20px; border-radius: 50%; cursor: pointer; font-size: 16px; line-height: 1; transition: background 0.2s; font-family: monospace;';
                    closeBtn.onmouseover = function() {{ this.style.background = 'rgba(255,255,255,0.3)'; }};
                    closeBtn.onmouseout = function() {{ this.style.background = 'rgba(255,255,255,0.2)'; }};
                    closeBtn.onclick = function() {{ banner.style.display = 'none'; }};
                    
                    banner.appendChild(icon);
                    banner.appendChild(text);
                    banner.appendChild(closeBtn);
                    document.body.appendChild(banner);
                    
                }} else {{
                    // Enhanced watermark (default)
                    const watermark = document.createElement('div');
                    watermark.id = 'juldeptrai-watermark';
                    watermark.style.cssText = 'position: fixed; bottom: 16px; right: 16px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.5), rgba(118, 75, 162, 0.5)); backdrop-filter: blur(10px); color: white; padding: 10px 16px; border-radius: 8px; font-size: 15px; font-weight: 600; z-index: 2147483647; pointer-events: none; user-select: none; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); display: flex; align-items: center; gap: 8px; font-family: monospace; animation: juldeptrai-pulse 2s ease-in-out infinite;';
                    
                    const icon = document.createElement('span');
                    icon.textContent = '🎯';
                    icon.style.cssText = 'font-size: 18px; animation: juldeptrai-rotate 3s linear infinite;';
                    
                    const text = document.createElement('span');
                    text.textContent = '{safe_profile_name}';
                    
                    watermark.appendChild(icon);
                    watermark.appendChild(text);
                    document.body.appendChild(watermark);
                    
                    // Add animation styles
                    if (!document.getElementById('juldeptrai-watermark-styles')) {{
                        const styleEl = document.createElement('style');
                        styleEl.id = 'juldeptrai-watermark-styles';
                        styleEl.textContent = '@keyframes juldeptrai-pulse {{ 0%, 100% {{ box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }} 50% {{ box-shadow: 0 4px 25px rgba(102, 126, 234, 0.6); }} }} @keyframes juldeptrai-rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}';
                        document.head.appendChild(styleEl);
                    }}
                }}
                
            }} catch(e) {{ /* Silent fail */ }}
        }}
        
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', createWatermark);
        }} else {{
            createWatermark();
        }}

    }} catch(e) {{ console.error("AntiDetect Error", e); }}
}})();
'''
