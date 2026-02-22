"""
Stealth Browser - Playwright-based browser with AntiDetect Core fingerprint injection
Optimized for Amazon checking with full fingerprint spoofing

Uses playwright + custom fingerprint injection (by juldeptrai)
"""

import asyncio
import random
import os
import sys
import tempfile
import shutil
import aiohttp
from playwright.async_api import async_playwright, BrowserContext, Page

# Import our AntiDetect core module
from antidetect_core import generate_fingerprint, get_inject_script


async def get_timezone_from_proxy(proxy_config: dict, timeout: int = 10) -> tuple:
    """
    Get timezone and geolocation from proxy IP using ip-api.com
    
    Args:
        proxy_config: Dict with 'server', optionally 'username', 'password'
        timeout: Request timeout in seconds
    
    Returns:
        tuple: (timezone, geolocation_dict) or ("America/New_York", None) on failure
    """
    default_tz = "America/New_York"
    default_geo = None
    
    if not proxy_config or 'server' not in proxy_config:
        return default_tz, default_geo
    
    try:
        # Build proxy URL for aiohttp
        server = proxy_config['server']
        if proxy_config.get('username') and proxy_config.get('password'):
            # Insert auth into proxy URL: http://user:pass@host:port
            from urllib.parse import urlparse
            parsed = urlparse(server)
            proxy_url = f"{parsed.scheme}://{proxy_config['username']}:{proxy_config['password']}@{parsed.netloc}"
        else:
            proxy_url = server
        
        # Query ip-api.com through proxy
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'http://ip-api.com/json/?fields=status,timezone,lat,lon,city,country',
                proxy=proxy_url,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'success':
                        timezone = data.get('timezone', default_tz)
                        geolocation = {
                            'latitude': data.get('lat'),
                            'longitude': data.get('lon'),
                        }
                        print(f"[Proxy Geo] Detected: {data.get('city', 'Unknown')}, {data.get('country', 'Unknown')} - TZ: {timezone}")
                        return timezone, geolocation
        
        return default_tz, default_geo
    
    except Exception as e:
        print(f"[Proxy Geo] Failed to detect timezone: {e}")
        return default_tz, default_geo


class StealthBrowser:
    """
    A stealth browser class that wraps Playwright with AntiDetect fingerprint injection.
    Uses Google Chrome channel with persistent context for best stealth.
    Fingerprint spoofing: Canvas, Audio, WebRTC, Hardware, Timezone, Geolocation, Language.
    """
    
    def __init__(
        self,
        max_retries=3,
        window_position=None,
        proxy=None,
        headless=False,
        timezone: str = "America/New_York",
        language: str = "en-US",
        geolocation: dict = None,
        profile_name: str = None,
        watermark_style: str = "enhanced",
        webgl_spoof: bool = True,  # Set False to avoid Pixelscan masking detection
        auto_timezone: bool = False,  # Auto-detect timezone from proxy IP
    ):
        """
        Initialize the StealthBrowser with AntiDetect features.
        
        Args:
            max_retries: Maximum retry attempts for navigation
            window_position: Dict with 'x', 'y', 'width', 'height' keys for window
            proxy: Proxy configuration (dict with 'server', 'username', 'password' or string)
            headless: Whether to run browser in headless mode
            timezone: IANA timezone string (e.g., "America/New_York")
            language: Browser language (e.g., "en-US")
            geolocation: Optional dict with 'latitude', 'longitude' for geo spoofing
            profile_name: Name displayed in watermark (optional)
            watermark_style: 'enhanced' (bottom-right) or 'banner' (top bar)
            webgl_spoof: If True, spoof WebGL (may trigger masking detection on Pixelscan)
                         If False, use real GPU (no masking but reveals hardware)
            auto_timezone: If True, detect timezone and geolocation from proxy IP automatically
        """
        self.playwright = None
        self.context = None  # In persistent mode, context IS the browser
        self.page = None
        self.on_waf = None  # Optional callback for WAF detection
        self.user_data_dir = None  # Temp directory for browser profile
        
        self.max_retries = max_retries
        self.window_position = window_position
        self.proxy = proxy
        self.headless = headless
        
        # AntiDetect settings
        self.timezone = timezone
        self.language = language
        self.geolocation = geolocation
        self.profile_name = profile_name or f"Profile-{random.randint(1000, 9999)}"
        self.watermark_style = watermark_style
        self.webgl_spoof = webgl_spoof
        self.auto_timezone = auto_timezone
        
        # Generated fingerprint (set during start)
        self.fingerprint = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def start(self):
        """
        Start the browser with Playwright + AntiDetect fingerprint injection.
        Uses launch_persistent_context with Google Chrome for maximum stealth.
        """
        try:
            # Initialize Playwright if not already done
            if not self.playwright:
                self.playwright = await async_playwright().start()
            
            # Create a temp directory for user data (persistent context requirement)
            self.user_data_dir = tempfile.mkdtemp(prefix="antidetect_")
            
            # Auto-detect timezone from proxy if enabled
            effective_timezone = self.timezone
            effective_geolocation = self.geolocation
            
            if self.auto_timezone and self.proxy:
                proxy_config = self.proxy if isinstance(self.proxy, dict) else {'server': self.proxy}
                detected_tz, detected_geo = await get_timezone_from_proxy(proxy_config)
                effective_timezone = detected_tz
                if detected_geo and not self.geolocation:
                    effective_geolocation = detected_geo
            
            # Generate fingerprint with custom settings
            screen_width = None
            screen_height = None
            if self.window_position:
                screen_width = self.window_position.get('width', 1280)
                screen_height = self.window_position.get('height', 800)
            
            self.fingerprint = generate_fingerprint(
                timezone=effective_timezone,
                language=self.language,
                geolocation=effective_geolocation,
                screen_width=screen_width,
                screen_height=screen_height,
                webgl_spoof=self.webgl_spoof,
            )
            
            # Generate injection script
            inject_script = get_inject_script(
                self.fingerprint,
                self.profile_name,
                self.watermark_style,
            )
            
            # Configure proxy
            proxy_config = None
            if self.proxy:
                try:
                    if isinstance(self.proxy, dict):
                        if 'server' in self.proxy:
                            server = self.proxy['server']
                            proxy_config = {'server': server}
                            print(f"[Browser] Using proxy: {server}")
                        
                        if self.proxy.get('username') and self.proxy.get('password'):
                            proxy_config['username'] = self.proxy['username']
                            proxy_config['password'] = self.proxy['password']
                            print(f"[Browser] Using proxy with auth: {self.proxy['username']}")
                    
                    elif isinstance(self.proxy, str):
                        proxy_config = {'server': self.proxy}
                        print(f"[Browser] Using proxy: {self.proxy}")
                
                except Exception as proxy_error:
                    print(f"[Browser] Proxy error: {proxy_error}, continuing without proxy")
            
            # Build launch args - comprehensive anti-detection flags
            launch_args = [
                '--disable-blink-features=AutomationControlled',  # Hide webdriver detection
                '--disable-features=IsolateOrigins,site-per-process',
                '--force-webrtc-ip-handling-policy=disable_non_proxied_udp',
                '--no-first-run',                    # Skip first run wizard
                '--no-default-browser-check',        # Skip default browser check
                '--disable-background-timer-throttling',  # Prevent background tab throttling
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-dev-shm-usage',           # Reduce shared memory usage
                '--disk-cache-size=52428800',        # Limit disk cache to 50MB
                '--media-cache-size=52428800',       # Limit media cache to 50MB
            ]
            
            # Add window position args if provided and not headless
            if self.window_position and not self.headless:
                x = self.window_position.get('x', 0)
                y = self.window_position.get('y', 0)
                width = self.window_position.get('width', 960)
                height = self.window_position.get('height', 540)
                launch_args.extend([
                    f"--window-position={x},{y}",
                    f"--window-size={width},{height}",
                ])
            
            # Add language args
            launch_args.extend([
                f"--lang={self.language}",
                f"--accept-lang={self.language}",
            ])
            
            # Set environment for timezone (works on macOS/Linux)
            env = os.environ.copy()
            if effective_timezone and effective_timezone != 'Auto':
                env['TZ'] = effective_timezone
            
            # Launch persistent context with Chrome
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                channel="chrome",           # Use real Google Chrome
                headless=self.headless,
                no_viewport=True,           # Don't override viewport (more natural)
                args=launch_args if launch_args else None,
                proxy=proxy_config,
                timezone_id=effective_timezone if effective_timezone != 'Auto' else None,
                locale=self.language,
                env=env,
                # DO NOT add custom user_agent - let Chrome use native
            )
            
            # Inject anti-detect script into all pages
            await self.context.add_init_script(inject_script)
            
            # Get first page or create new one
            if self.context.pages:
                self.page = self.context.pages[0]
            else:
                self.page = await self.context.new_page()
            
            print(f"[Browser] Started with AntiDetect Core (Profile: {self.profile_name}, TZ: {effective_timezone}, Lang: {self.language})")
        
        except Exception as error:
            print(f"[Browser] Error starting browser: {error}")
            await self.close()
            raise error
    
    async def goto(self, url, **kwargs):
        """Navigate to a URL with a random delay."""
        await asyncio.sleep(random.uniform(0.5, 1.5))
        return await self.page.goto(url, **kwargs)
    
    async def human_type(self, selector, text):
        """
        Type text in a human-like manner with random delays between keystrokes.
        """
        await self.page.click(selector)
        await asyncio.sleep(random.uniform(0.05, 0.15))
        
        for char in text:
            await self.page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.02, 0.08))
    
    async def human_click(self, selector):
        """
        Click an element in a human-like manner (hover then click).
        """
        await self.page.hover(selector)
        await asyncio.sleep(random.uniform(0.05, 0.25))
        await self.page.click(selector)
    
    async def random_mouse_movement(self):
        """Perform random mouse movements to simulate human behavior."""
        for _ in range(random.randint(2, 5)):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            await self.page.mouse.move(x, y)
            await asyncio.sleep(random.uniform(0.1, 0.3))
    
    async def close(self):
        """Close and clean up all browser resources."""
        try:
            if self.page:
                await self.page.close()
                self.page = None
        except:
            pass
        
        try:
            if self.context:
                await self.context.close()
                self.context = None
        except:
            pass
        
        try:
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
        except:
            pass
        
        # Clean up temp user data directory
        try:
            if self.user_data_dir and os.path.exists(self.user_data_dir):
                shutil.rmtree(self.user_data_dir, ignore_errors=True)
                self.user_data_dir = None
        except:
            pass
    
    async def check_captcha_or_block(self):
        """
        Check if the page shows a captcha or is blocked.
        
        Returns:
            True if captcha/block detected, False otherwise
        """
        # Check for "Click the button below to continue shopping" message
        try:
            element = await self.page.wait_for_selector(
                'h4:has-text("Click the button below to continue shopping")',
                timeout=3000
            )
            if element:
                print("[Browser] Detected: 'Click the button below to continue shopping' - Browser blocked!")
                return True
        except:
            pass
        
        # Amazon WAF / Captcha indicators
        captcha_selectors = [
            '#aacb-captcha-header',
            'h1:has-text("Solve this puzzle")',
            'iframe[src*="captcha"]',
            '[id*="captcha"]'
        ]
        
        for selector in captcha_selectors:
            try:
                element = await self.page.wait_for_selector(selector, timeout=1500)
                if element:
                    print("[Browser] Detected: Amazon WAF/Captcha -", selector)
                    return True
            except:
                pass
        
        # Check for "Sorry! We couldn't find that page" error
        try:
            element = await self.page.wait_for_selector(
                'img[alt*="Sorry! We couldn\'t find that page"]',
                timeout=3000
            )
            if element:
                print("[Browser] Detected: 'Sorry! We couldn't find that page' - Page error!")
                return True
        except:
            pass
        
        # URL-based hints
        try:
            current_url = self.page.url.lower()
            if 'captcha' in current_url or '/ap/cvf/' in current_url:
                return True
        except:
            pass
        
        return False
    
    async def restart_browser(self):
        """Restart the browser with a fresh session."""
        print('[Browser] Restarting browser...')
        await self.close()
        await asyncio.sleep(random.uniform(1, 2))
        await self.start()
    
    async def goto_with_retry(self, url, **kwargs):
        """
        Navigate to a URL with automatic retry on captcha/block detection.
        
        Returns:
            True on success, False if max retries exceeded
        """
        for attempt in range(self.max_retries):
            try:
                print(f"[Browser] Attempt {attempt + 1}: Navigating to {url[:50]}...")
                await self.goto(url, **kwargs)
                
                if await self.check_captcha_or_block():
                    # Optional external handler to rotate proxy on WAF
                    try:
                        if getattr(self, 'on_waf', None):
                            await self.on_waf()
                    except Exception as waf_error:
                        print(f"[Browser] on_waf handler error: {waf_error}")
                    
                    if attempt < self.max_retries - 1:
                        await self.restart_browser()
                        continue
                    else:
                        print(f"[Browser] Max retries reached for {url}")
                        return False
                
                return True
            
            except Exception as nav_error:
                print(f"[Browser] Navigation error: {nav_error}")
                
                if attempt < self.max_retries - 1:
                    await self.restart_browser()
                    continue
                else:
                    print(f"[Browser] Max retries reached, giving up")
                    return False
        
        return False


async def patch_context(context):
    """
    Apply stealth patches to an existing browser context.
    Note: With AntiDetect Core, patches are applied via add_init_script.
    """
    print('[Stealth] Context ready with AntiDetect Core fingerprint injection')